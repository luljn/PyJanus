# Event Skill

from .Skill import Skill
from capacities.EventCapacity import EventCapacity

class EventSkill(Skill, EventCapacity) :
    
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