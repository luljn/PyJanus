# class Kernel

from __future__ import annotations
from typing import Optional, Type

from .ArgType import ArgType
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
        self.__services.extend([DirectoryService(), EventService(), ExecutionService(), LifeCycleService()])
    
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
    
    # Stop the kernel.
    def stop(self) -> None :
        
        print("\n[INFO] Kernel stoped without any error :) !\n")
        self.__running = False
    
    #
    def getService(self, serviceClass: Type[Service])->Service :
        
        for service in self.__services : 
            if(isinstance(service, serviceClass)) :
                print(f"service class : {service.__class__}") # To remove (it is just for testing).
                return service
    
    # Spawn an agent.
    def spawn(self, argType: ArgType, fileOrModuleName: str)-> None :
        
        self.getService(LifeCycleService).spawnAgent()
        match(argType) :
            case ArgType.FILE :
                pass
            case ArgType.MODULE :
                pass
    
    #
    def getDefaultSpace(self)->Space :
        
        return self.__defaultSpace