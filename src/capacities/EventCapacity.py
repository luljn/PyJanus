# Event Capacity.

from .Capacity import Capacity
from agent.Agent import Agent
from event.Event import Event
from space.Space import Space

"""Capability allowing the agent to send and receive events
    in the spaces in which it participates.
"""
class EventCapacity(Capacity) :
    
    """Broadcasts an event to the agent's default space.
        :param eventType: The instance of the event to broadcast.
    """
    @staticmethod
    def emitEvent(user: Agent, eventType:Event)-> None :
        
        from skills.EventSkill import EventSkill
        user.getSkill(EventSkill).emit(user, eventType)
    
    """Processes an received event.
    """
    @staticmethod
    def receive(user: Agent, event:Event)-> None :
        
        from skills.EventSkill import EventSkill
        user.getSkill(EventSkill).receive(user, event)
    
    """To register an agent in a space.
    """
    @staticmethod
    def registerInSpace(user: Agent, space: Space)-> None :
        
        from skills.EventSkill import EventSkill
        user.getSkill(EventSkill).registerInSpace(user, space)
    
    """It awakens the agent's behaviors that are awaiting this specific event.
    """
    @staticmethod
    def wake(user: Agent, event:Event)-> None :
        
        pass