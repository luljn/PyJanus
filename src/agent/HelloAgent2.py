from typing import Callable, Type
from uuid import UUID
from .Agent import Agent
from services.LifeCycleService import Initialize
from io.sarl.sre.pysarlvm.lang.core import Lifecycle

class HelloAgent2(Agent):
    def __init__(self, id : UUID = None):
        super().__init__(id)
        # Define the mapping for all the function from the used capacities
        self.killMe = lambda: self.getSkill(Type[Lifecycle]).killMe()

    # Nothing to generates for the SARL statement:
    # uses Lifecycle

    # This method is called by the Event Service
    def __guard_Initialize__(self, occurrence : Initialize, _event_handlers : list[Callable[[Initialize],None]]):
        it = occurrence
        _event_handlers.append(self.__on_Initialize__)

    def __on_Initialize__(self, occurrence : Initialize):
        print("Hello World")
        # Call the function killMe defined in the capacity Lifecycle
        self.killMe()

