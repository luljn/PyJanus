# Event Capacity

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .Capacity import Capacity
from agent.Agent import Agent
from event.Event import Event
from space.Space import Space
if TYPE_CHECKING : 
    from skills.EventSkill import EventSkill

"""
    Capability allowing the agent to send and receive events
    in the spaces in which it participates.
"""
class EventCapacity(Capacity) :
    
    """ def __init__(self,owner:Agent=None) :
        
        super().__init__(owner) """
    
    """
        Broadcasts an event to the agent's default space.
        :param event: The instance of the event to broadcast.
    """
    @staticmethod
    def emitEvent(user: Agent, eventType:Event)-> None :
        from skills.EventSkill import EventSkill
        user.getSkill(EventSkill).emit(user, eventType)
    
    """ 
        Processes an received event.
    """
    @abstractmethod
    def receive(self, user: Agent, event:Event)-> None :
        pass
    
    """
        It awakens the agent's behaviors that are awaiting this specific event.
    """
    @abstractmethod
    def wake(self, user: Agent, event:Event)-> None :
        pass
    
    """
        To register an agent in a space.
    """
    @staticmethod
    def registerInSpace(user: Agent, space: Space)-> None :
        from skills.EventSkill import EventSkill
        user.getSkill(EventSkill).registerInSpace(user, space)
    
    """
        To unregister an agent from a space.
    """
    @staticmethod
    def unregisterFromSpace(user: Agent, space: Space)-> None :
        from skills.EventSkill import EventSkill
        user.getSkill(EventSkill).registerInSpace(user, space)