# class Kernel

from __future__ import annotations
from asyncio import run
from typing import Optional, Type

from .ArgType import ArgType
from agent.Agent import Agent
from services.Service import Service
from services.DirectoryService import DirectoryService
from services.EventService import EventService
from services.ExecutionService import ExecutionService
from services.LifeCycleService import LifeCycleService
from space.Space import Space

"""
    _summary_ : 
    
"""
class Kernel : 
    
    __instance: Optional[Kernel] = None
    
    # Constructor.
    def __init__(self) :
        
        self.__services: list[Service] = []
        self.__defaultSpace: Space = Space()
        self.__running: bool = False
        self.__mainThread = None
        
        # Adding services to the services list.
        self.__services.extend([DirectoryService(), EventService(), ExecutionService(), LifeCycleService(agent_concrete_class=Agent)])
    
    # Return an unique instance of the Kernel.
    @staticmethod
    def getInstance()->Kernel : 
        
        if (Kernel.__instance is None) :
            Kernel.__instance = Kernel()
        
        return Kernel.__instance
    
    # Start the kernel.
    def start(self) -> None : 
        
        self.__running = True
        print("[INFO] Kernel started successfully :) !\n")
        # Starting all the services.
        for service in self.__services :
            run(service.start_async())
    
    # Stop the kernel.
    def stop(self) -> None :
        
        # Starting all the services.
        """ for service in self.__services :
            run(service.stop_async()) """
        print("\n[INFO] Kernel stoped without any error :) !\n")
        self.__running = False
    
    # To get a service with its Type.
    def getService(self, serviceClass: Type[Service])->Service :
        
        for service in self.__services : 
            if(isinstance(service, serviceClass)) :
                #print(f"service class : {service.__class__}") # To remove (it is just for testing).
                return service
    
    # Spawn an agent.
    def spawn(self, argType: ArgType, fileOrModuleName: str)-> None :
        
        match(argType) :
            case ArgType.FILE :
                run(self.getService(LifeCycleService).spawnAgent(agent_class=self.__fileToModule(fileOrModuleName)))
            case ArgType.MODULE :
                run(self.getService(LifeCycleService).spawnAgent(agent_class=fileOrModuleName))
    
    # Return the default space.
    def getDefaultSpace(self)->Space :
        
        return self.__defaultSpace
    
    # Convert a file name to module name.
    def __fileToModule(self, file_path : str) -> str:
        """
        Transform a file name (ex: 'agent/HelloAgent.py') 
        in module dot notation (ex: 'agent.HelloAgent').
        """
        if file_path.endswith('.py'):
            file_path = file_path[:-3]
        
        module = file_path.replace('/', '.').replace('\\', '.')
        
        return module.strip('.')