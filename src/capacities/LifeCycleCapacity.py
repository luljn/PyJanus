# LifeCycle Capacity.

from agent.Agent import Agent
from .Capacity import Capacity

"""Capacity defining the actions related to the agent's lifecycle.
"""
class LifeCycleCapacity(Capacity) :
    
    """Creates a new agent instance of a given type.
    """
    @staticmethod
    async def spawn(user: Agent, agentType: str) -> None :
        
        from skills.SpawnSkill import SpawnSkill
        await(user.getSkill(SpawnSkill).spawn(agentType))
    
    """Demands the arrest and destruction of an agent.
    """
    @staticmethod
    async def killMe(user: Agent) -> None :
        
        from skills.KillSkill import KillSkill
        await(user.getSkill(KillSkill).killMe(user))
    
    """Creates an agent in a specific context.
    """
    @staticmethod
    async def spawn_in_context(user: Agent, agent: Agent, context_id, *args) -> None :
        
        pass 