# LifeCycle Service

from .Service import Service

class LifeCycleService(Service) : 
    
    #
    def __init__(self) :
        
        super().__init__()
    
    #
    def startAsync(self) :
        
        pass
    
    #
    def stopAsync(self) :
        
        pass
    
    #
    def awaitRunning(self) :
        
        pass
    
    #
    def spawnAgent(self)-> None :
        
        pass
    
    #
    def killAgent(self)-> bool :
        
        return True