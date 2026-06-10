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
    @staticmethod
    async def spawn(user: Agent, agentType: str) -> None :
        
        from skills.SpawnSkill import SpawnSkill
        await(user.getSkill(SpawnSkill).spawn(agentType))
    
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