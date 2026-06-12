# Kill Skill

from asyncio import create_task

from .Skill import Skill
from agent.Agent import Agent
from capacities.LifeCycleCapacity import LifeCycleCapacity
from kernel.Kernel import Kernel
from services.LifeCycleService import LifeCycleService

class KillSkill(Skill, LifeCycleCapacity) :
    
    # Constructor
    def __init__(self) :
        
        super().__init__()
    
    
    """
        Demands the arrest and destruction of an agent.
    """
    def killMe(self, agent: Agent) -> None :
        
        create_task(Kernel.getInstance().getService(LifeCycleService).killAgent(agent))