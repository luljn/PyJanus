from typing import Callable

from .Agent import Agent
from .AgentState import AgentState
from services.LifeCycleService import Initialize
from skills.KillSkill import KillSkill

class HelloAgent2(Agent):
    def __init__(self):
        super().__init__()
        # Define the mapping for all the function from the used capacities
        #self.killMe = lambda: self.getSkill(KillSkill).killMe(self)

    # Nothing to generates for the SARL statement:
    # uses Lifecycle

    # This method is called by the Event Service
    def __guard_Initialize__(self, occurrence : Initialize, _event_handlers : list[Callable[[Initialize],None]]):
        it = occurrence
        _event_handlers.append(self._onInitialize)

    def _onInitialize(self, occurrence : Initialize = None) :
        super()._onInitialize()
        self.setState(AgentState.RUNNING)
        print("[" + self.getName() + "] Hello World 2\n")
        # Call the function killMe defined in the capacity Lifecycle
        self.killMe()
    
    def _onDestroy(self)-> None :
        
        super()._onDestroy()