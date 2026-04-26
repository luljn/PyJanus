###

from abc import ABC, abstractmethod


class Service(ABC) : 
    
    #
    @abstractmethod
    def startAsync(self) :
        
        self
    
    #
    @abstractmethod
    def stopAsync(self) :
        
        self
    
    #
    @abstractmethod
    def awaitRunning(self) :
        
        self