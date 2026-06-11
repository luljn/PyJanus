from typing import Callable, Type
from uuid import UUID
from .Agent import Agent
from .AgentState import AgentState
from services.EventService import EventService
from services.LifeCycleService import Initialize
from services.LifeCycleService import LifeCycleService
from skills.EventSkill import EventSkill
from skills.SpawnSkill import SpawnSkill
from .HelloAgent4 import HelloAgent4
from event.AgentSpawned import AgentSpawned
from event.MyEvent import MyEvent
from space.Space import Space

class HelloAgent3(Agent):
    def __init__(self, id : UUID = None):
        super().__init__(id)
        # Define the mapping for all the function from the used capacities
        self.killMe = lambda: self.getSkill(Type[LifeCycleService]).killMe()
        self.spawn = lambda agent_type, *args: self.getSkill(Type[SpawnSkill]).spawnAgent(agent_type, *args)
        #self.emit = lambda event, filter=None: self.getSkill(EventSkill).emit(event, filter)
    
    # Nothing to generates for the SARL statement:
    # uses Lifecycle
    
    # This method is called by the Event Service
    def __guard_Initialize__(self, occurrence : Initialize, _event_handlers : list[Callable[[Initialize],None]]):
        it = occurrence
        _event_handlers.append(self._onInitialize)

    def _onInitialize(self, occurrence : Initialize = None):
        super()._onInitialize()
        self.setState(AgentState.RUNNING)
        print(f"[{self.getName()}] Hello World 3\n")
        #self.spawn(Type[HelloAgent4])
        self.spawnAgent(HelloAgent4.__module__)
        self.__on_AgentSpawned__(AgentSpawned(source=self, data=f"[Agent {self.getName()}] has spawned {HelloAgent4.__module__} Type"))

    def __guard_AgentSpawned__(self, occurrence: AgentSpawned, _event_handlers: list[Callable[[AgentSpawned], None]]):
        it = occurrence
        _event_handlers.append(self.__on_AgentSpawned__)

    def __on_AgentSpawned__(self, occurrence: AgentSpawned):
        print("The other agent was spawned")
        self.emit(occurrence)
        #self.killMe()
    
    def _onDestroy(self)-> None :
        
        pass
