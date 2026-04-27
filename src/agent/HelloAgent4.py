from typing import Callable, Type
from uuid import UUID
from io.sarl.sre.pysarlvm.lang.core import Agent
from io.sarl.sre.pysarlvm.lang.core import Lifecycle

class HelloAgent4(Agent):
    def __init__(self, id : UUID = None):
        super().__init__(id)
        self.killMe = lambda: self.getSkill(Type[Lifecycle]).killMe()

    # This method is called by the Event Service
    def __guard_MyEvent__(self, occurrence : MyEvent, _event_handlers : list[Callable[[MyEvent],None]]):
        it = occurrence
        _event_handlers.append(self.__on_MyEvent__)

    def __on_MyEvent__(self, occurrence : MyEvent):
        print("Received my event with " + occurrence.value1 + " and " + occurrence.value2)
        self.killMe()

