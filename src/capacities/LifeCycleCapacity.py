# LifeCycle Capacity

from abc import ABC

from agent.Agent import Agent
from .Capacity import Capacity

class LifeCycleCapacity(ABC, Capacity) :
    
    #
    def __init__(self) :
        
        super().__init__()
    
    #
    def spawn(a: Agent)-> None :
        
        pass
    
    #
    def killMe()-> None : 
        
        pass