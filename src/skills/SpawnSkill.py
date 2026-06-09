# Spawn Skill

from asyncio import run

from .Skill import Skill
from agent.Agent import Agent
from capacities.LifeCycleCapacity import LifeCycleCapacity
from kernel.Kernel import Kernel
from services.LifeCycleService import LifeCycleService

class SpawnSkill(Skill, LifeCycleCapacity) :
    
    # Constructor.
    def __init__(self) :
        
        super().__init__()
    
    """
        Creates a new agent instance of a given type.
    """
    async def spawn(self, agentType: str) -> None :
        
        await(Kernel.getInstance().getService(LifeCycleService).spawnAgent(agent_class=agentType))
    
    """
        Demands the arrest and destruction of the current agent.
    """
    def killme(self, user: Agent) -> None :
        
        pass
    
    """ 
        Creates an agent in a specific context.
    """
    def spawn_in_context(self, user: Agent, agent: Agent, context_id, *args) -> None :
        pass 