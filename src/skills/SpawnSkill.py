# Spawn Skill.

from .Skill import Skill
from agent.Agent import Agent
from capacities.LifeCycleCapacity import LifeCycleCapacity
from kernel.Kernel import Kernel
from services.LifeCycleService import LifeCycleService

"""_summary_ : Skill used by an agent to spawn another agent.
"""
class SpawnSkill(Skill, LifeCycleCapacity) :
    
    # Constructor.
    def __init__(self) :
        
        super().__init__()
    
    """Spawn a new agent instance of a given type.
    """
    async def spawn(self, agentType: str) -> None :
        
        await(Kernel.getInstance().getService(LifeCycleService).spawnAgent(agent_class=agentType))
    
    """Spawn an agent in a specific context.
    """
    async def spawn_in_context(self, user: Agent, agent: Agent, context_id, *args) -> None :
        
        pass 