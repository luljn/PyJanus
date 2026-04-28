from typing import Callable
from uuid import UUID
from .Agent import Agent
from Agent import Initialize

class HelloAgent(Agent):
    
    def __init__(self, id : UUID = None):
        super().__init__(id, f"HelloAgent_{id}")

    # This method is called by the Event Service
    def __guard_Initialize__(self, occurrence : Initialize, _event_handlers : list[Callable[[Initialize],None]]):
        it = occurrence
        _event_handlers.append(self.__onInitialize)

    def __onInitialize(self, occurrence : Initialize):
        print("Hello World")
