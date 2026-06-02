from typing import Callable, Type, Any
from uuid import UUID
from .Agent import Agent
from .AgentState import AgentState
from services.EventService import EventService
from services.LifeCycleService import Initialize
from services.LifeCycleService import LifeCycleService
from .HelloAgent4 import HelloAgent4
from event.Event import AgentSpawned
from event.MyEvent import MyEvent
from space.Space import Space
""" from io.sarl.sre.pysarlvm.lang.core import Agent
from io.sarl.sre.pysarlvm.lang.core import AgentSpawned
from io.sarl.sre.pysarlvm.lang.core import Initialize
from io.sarl.sre.pysarlvm.lang.core import Lifecycle
from io.sarl.sre.pysarlvm.lang.core import DefaultContextInteractions """

class HelloAgent3(Agent):
    def __init__(self, id : UUID = None):
        super().__init__(id)
        # Define the mapping for all the function from the used capacities
        self.killMe = lambda: self.getSkill(Type[LifeCycleService]).killMe()
        self.spawn = lambda agent_type, *args: self.getSkill(Type[LifeCycleService]).spawn(agent_type, *args)
        self.emit = lambda event, filter=None: self.getSkill(Type[EventService]).emit(event, filter)

    # Nothing to generates for the SARL statement:
    # uses Lifecycle

    # This method is called by the Event Service
    def __guard_Initialize__(self, occurrence : Initialize, _event_handlers : list[Callable[[Initialize],None]]):
        it = occurrence
        _event_handlers.append(self._onInitialize)

    def _onInitialize(self, occurrence : Initialize = None):
        self.setState(AgentState.RUNNING)
        print(f"[{self.getName()}] Hello World 3\n")
        #self.spawn(Type[HelloAgent4])

    def __guard_AgentSpawned__(self, occurrence: AgentSpawned, _event_handlers: list[Callable[[AgentSpawned], None]]):
        it = occurrence
        _event_handlers.append(self.__on_AgentSpawned__)

    def __on_AgentSpawned__(self, occurrence: AgentSpawned):
        print("The other agent was spawned")
        #self.emit(MyEvent())
        #self.killMe()
    
    def _onDestroy(self)-> None :
        
        pass
    
    def _receive(self)-> None :
        
        pass
    
    def _inSpace(self, space: Space)-> None :
        
        if self.__id in space.getParticipants() : return True
        return False
    
    def _leave(self)-> None :
        
        pass

