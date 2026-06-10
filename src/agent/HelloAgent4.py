from typing import Callable, Type
from uuid import UUID
from .Agent import Agent
from .AgentState import AgentState
from event.MyEvent import MyEvent
from services.LifeCycleService import LifeCycleService
from services.LifeCycleService import Initialize
from skills.KillSkill import KillSkill

class HelloAgent4(Agent):
    def __init__(self, id : UUID = None):
        super().__init__(id)
        self.killMe = lambda: self.getSkill(Type[KillSkill]).killMe()

    # This method is called by the Event Service
    def __guard_MyEvent__(self, occurrence : MyEvent, _event_handlers : list[Callable[[MyEvent],None]]):
        it = occurrence
        _event_handlers.append(self.__on_MyEvent__)

    def __on_MyEvent__(self, occurrence : MyEvent):
        print("Received my event with " + occurrence.value1 + " and " + occurrence.value2)
        self.killMe()
    
    def _onInitialize(self, occurrence : Initialize = None) :
        super()._onInitialize()
        self.setState(AgentState.RUNNING)
        print(f"[{self.getName()}] Hello World 4\n")
        # Call the function killMe defined in the capacity Lifecycle
        #self.killMe()
    
    def _onDestroy(self)-> None :
        
        pass