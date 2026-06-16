# Event Skill

from .Skill import Skill
from agent.Agent import Agent
from capacities.EventCapacity import EventCapacity
from event.Event import Event
from kernel.Kernel import Kernel
from services.EventService import EventService
from services.DirectoryService import DirectoryService
from space.Space import Space

class EventSkill(Skill, EventCapacity) :
    
    # Contructor.
    def __init__(self) :
        
        super().__init__()
    
    # To  emit an event.
    def emit(self, agent: Agent, eventType: Event)-> None :
        
        """ Kernel.getInstance().getDefaultSpace().send(
            Kernel.getInstance().getService(EventService).emit(event=eventType, source=agent)) """
        Kernel.getInstance().getService(EventService).emit(event=eventType, source=agent)
    
    # To process an received event.
    def receive(self, agent: Agent, event: Event)-> None : 
        
        Kernel.getInstance().getService(EventService).receive(agent, event)
    
    #
    def wake(self)-> None : 
        
        pass
    
    # To register an agent in a space and in the global directory.
    def registerInSpace(self, agent: Agent, space: Space)-> None :
        
        Kernel.getInstance().getService(EventService).registerAgent(agent, space)
        Kernel.getInstance().getService(DirectoryService).register_agent(agent)