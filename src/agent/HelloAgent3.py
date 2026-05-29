from typing import Callable, Type, Any
from uuid import UUID
from agent.Agent import Agent
from services.LifeCycleService import Initialize
from .HelloAgent4 import HelloAgent4
from services.LifeCycleService import AgentSpawned
from event.MyEvent import MyEvent
""" from io.sarl.sre.pysarlvm.lang.core import Agent
from io.sarl.sre.pysarlvm.lang.core import AgentSpawned
from io.sarl.sre.pysarlvm.lang.core import Initialize
from io.sarl.sre.pysarlvm.lang.core import Lifecycle
from io.sarl.sre.pysarlvm.lang.core import DefaultContextInteractions """

class HelloAgent3(Agent):
    def __init__(self, id : UUID = None):
        super().__init__(id)
        # Define the mapping for all the function from the used capacities
        """ self.killMe = lambda: self.getSkill(Type[Lifecycle]).killMe()
        self.spawn = lambda agent_type, *args: self.getSkill(Type[Lifecycle]).spawn(agent_type, *args)
        self.emit = lambda event, filter=None: self.getSkill(Type[DefaultContextInteractions]).emit(event, filter) """

    # Nothing to generates for the SARL statement:
    # uses Lifecycle

    # This method is called by the Event Service
    def __guard_Initialize__(self, occurrence : Initialize, _event_handlers : list[Callable[[Initialize],None]]):
        it = occurrence
        _event_handlers.append(self.__on_Initialize__)

    def __on_Initialize__(self, occurrence : Initialize):
        print("Hello World")
        #self.spawn(Type[HelloAgent4])

    def __guard_AgentSpawned__(self, occurrence: AgentSpawned, _event_handlers: list[Callable[[AgentSpawned], None]]):
        it = occurrence
        _event_handlers.append(self.__on_AgentSpawned__)

    def __on_AgentSpawned__(self, occurrence: AgentSpawned):
        print("The other agent was spawned")
        #self.emit(MyEvent())
        #self.killMe()

