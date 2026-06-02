from typing import Callable
from .Agent import Agent
from .AgentState import AgentState
from services.LifeCycleService import Initialize
from space.Space import Space

class HelloAgent(Agent) :
    
    def __init__(self) :
        super().__init__()

    # This method is called by the Event Service
    def __guard_Initialize__(self, occurrence : Initialize, _event_handlers : list[Callable[[Initialize],None]]) :
        it = occurrence
        _event_handlers.append(self.__onInitialize)

    def _onInitialize(self, occurrence : Initialize = None) :
        #super._onInitialize(occurrence)
        self.setState(AgentState.RUNNING)
        print(f"[{self.getName()}] Hello World\n")
    
    def _onDestroy(self)-> None :
        
        pass
    
    def _receive(self)-> None :
        
        pass
    
    def _inSpace(self, space: Space)-> None :
        
        if self.__id in space.getParticipants() : return True
        return False
    
    def _leave(self)-> None :
        
        pass
