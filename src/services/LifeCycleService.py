###

from .Service import Service

class LifeCycleService(Service) : 
    
    #
    def __init__(self) :
        
        super().__init__()
    
    #
    def spawnAgent(self)-> None :
        
        pass
    
    #
    def killAgent(self)-> bool :
        
        return True