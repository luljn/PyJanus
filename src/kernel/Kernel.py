# kernel/Kernel.py - CORRECTED

from __future__ import annotations
from asyncio import run
from threading import Thread
from time import sleep
from typing import Optional, Type

from .ArgType import ArgType
from agent.Agent import Agent
from services.Service import Service
from services.DirectoryService import DirectoryService
from services.EventService import EventService
from services.ExecutionService import ExecutionService
from services.LifeCycleService import LifeCycleService
from space.Space import Space


class Kernel:
    
    __instance: Optional[Kernel] = None
    
    def __init__(self):
        self.__services: list[Service] = []
        self.__defaultSpace: Space = Space()
        self.__running: bool = False
        
        # Adding services to the services list.
        self.__services.extend([LifeCycleService(), DirectoryService(), ExecutionService(), EventService()])
    
    @staticmethod
    def getInstance() -> Kernel:
        if Kernel.__instance is None:
            Kernel.__instance = Kernel()
        return Kernel.__instance
    
    def start(self) -> None:
        self.__running = True
        print("[INFO] Kernel started successfully :) !\n")
        print("[INFO] Start services !\n")
        for service in self.__services:
            run(service.start_async())
        # Start EventService background thread (after all services have been "started")
        event_svc = self.getService(EventService)
        if event_svc:
            event_svc.start()   # This method starts the background event loop thread
        # If you need to join any thread, handle elsewhere
    
    def stop(self) -> None:
        try:
            for service in self.__services:
                run(service.stop_async())
            if self.__running:
                self.__running = False
                print("\n[INFO] Kernel stopped without any error :) !\n")
        except Exception:
            pass
    
    def getService(self, serviceClass: Type[Service]) -> Service:
        for service in self.__services:
            if isinstance(service, serviceClass):
                return service
        return None
    
    async def spawn(self, argType: ArgType, fileOrModuleName: str) -> None:
        match argType:
            case ArgType.FILE:
                await self.getService(LifeCycleService).spawnAgent(agent_class=self.__fileToModule(fileOrModuleName))
            case ArgType.MODULE:
                await self.getService(LifeCycleService).spawnAgent(agent_class=fileOrModuleName)
    
    def getDefaultSpace(self) -> Space:
        return self.__defaultSpace
    
    def getRunningState(self):
        return self.__running
    
    def __fileToModule(self, file_path: str) -> str:
        if file_path.endswith('.py'):
            file_path = file_path[:-3]
        module = file_path.replace('/', '.').replace('\\', '.')
        return module.strip('.')