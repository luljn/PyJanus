# Event Skill

from .Skill import Skill
from agent.Agent import Agent
from capacities.EventCapacity import EventCapacity
from kernel.Kernel import Kernel
from services.EventService import EventService
from services.DirectoryService import DirectoryService
from space.Space import Space

class EventSkill(Skill, EventCapacity) :
    
    #
    def __init__(self) :
        
        super().__init__()
    
    #
    def emit(self)-> None :
        
        pass
    
    #
    def receive(self)-> None : 
        
        pass
    
    #
    def wake(self)-> None : 
        
        pass
    
    # To register an agent in a space.
    def registerInSpace(self, agent: Agent, space: Space)-> None :
        
        Kernel.getInstance().getService(EventService).registerAgent(agent, space)
        Kernel.getInstance().getService(DirectoryService).register_agent(agent)