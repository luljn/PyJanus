# Event Capacity

from abc import ABC

from .Capacity import Capacity

class EventCapacity(ABC, Capacity) :
    
    #
    def __init__(self) :
        
        super().__init__()
    
    #
    def emit()-> None :
        
        pass
    
    #
    def receive()-> None : 
        
        pass
    
    #
    def wake()-> None : 
        
        pass