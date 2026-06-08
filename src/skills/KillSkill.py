# Kill Skill

from .Skill import Skill
from agent.Agent import Agent
from capacities.LifeCycleCapacity import LifeCycleCapacity

class KillSkill(Skill, LifeCycleCapacity) :
    
    #
    def __init__(self) :
        
        super().__init__()
    
        """
        Creates a new agent instance of a given type.
    """
    def spawn(self, user: Agent, agent: Agent) -> None :
        
        pass
    
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