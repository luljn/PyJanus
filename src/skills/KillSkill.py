# Kill Skill.

from .Skill import Skill
from agent.Agent import Agent
from capacities.LifeCycleCapacity import LifeCycleCapacity
from kernel.Kernel import Kernel
from services.LifeCycleService import LifeCycleService

"""_summary_ : Skill used by an agent to die.
"""
class KillSkill(Skill, LifeCycleCapacity) :
    
    # Constructor
    def __init__(self) :
        
        super().__init__()
    
    """Demands the arrest and destruction of an agent.
    """
    async def killMe(self, agent: Agent) -> None :
        
        await(Kernel.getInstance().getService(LifeCycleService).killAgent(agent))