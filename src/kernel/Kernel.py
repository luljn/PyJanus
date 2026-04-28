# class Kernel

from __future__ import annotations
from typing import Optional

from services.Service import Service
from space.Space import Space

"""
    _summary_ : 
    
"""
class Kernel : 
    
    __instance: Optional[Kernel] = None
    
    #
    def __init__(self):
        
        self.__services: list[Service] = []
        self.__defaultSpace: Space = Space()
        self.__running: bool = False
        self.__mainThread = None
    
    #
    @staticmethod
    def getInstance() : 
        
        if (Kernel.__instance is None) :
            Kernel.__instance = Kernel()
            
        return Kernel.__instance
    
    #
    def start(self) -> None : 
        
        self.__running = True
        print("Kernel started successfully :) !\n")
    
    #
    def stop(self) -> None :
        
        print("\nKernel stoped without error :) !\n")
        self.__running = False
    
    #
    def getService(self)->Service :
        pass
    
    #
    def spawn(self) :
        pass
    
    #
    def getDefaultSpace(self)->Space :
        
        return self.__defaultSpace