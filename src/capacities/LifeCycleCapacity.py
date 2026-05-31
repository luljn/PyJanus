# LifeCycle Capacity

from abc import ABC, abstractmethod

from agent.Agent import Agent
from .Capacity import Capacity

"""
    Capacity defining the actions related to the agent's lifecycle.
"""
class LifeCycleCapacity(Capacity) :
    
    """ def __init__(self, owner=None):
        super().__init__(owner) """
    
    """
        Creates a new agent instance of a given type.
    """
    @abstractmethod
    def spawn(self, user: Agent, agent: Agent) -> None :
        
        pass
    
    """
        Demands the arrest and destruction of the current agent.
    """
    @abstractmethod
    def killme(self, user: Agent) -> None :
        
        pass
    
    """ 
        Creates an agent in a specific context.
    """
    @abstractmethod
    def spawn_in_context(self, user: Agent, agent: Agent, context_id, *args) -> None :
        pass 