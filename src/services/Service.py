# abstract class Service

from abc import ABC, abstractmethod


class Service(ABC) : 
    
    #
    @abstractmethod
    def startAsync(self) :
        
        pass
    
    #
    @abstractmethod
    def stopAsync(self) :
        
        pass
    
    #
    @abstractmethod
    def awaitRunning(self) :
        
        pass