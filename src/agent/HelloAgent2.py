from typing import Callable, Type
from .Agent import Agent
from services.LifeCycleService import Initialize
from space.Space import Space
#from io.sarl.sre.pysarlvm.lang.core import Lifecycle

class HelloAgent2(Agent):
    def __init__(self):
        super().__init__()
        # Define the mapping for all the function from the used capacities
        #self.killMe = lambda: self.getSkill(Type[Lifecycle]).killMe()

    # Nothing to generates for the SARL statement:
    # uses Lifecycle

    # This method is called by the Event Service
    def __guard_Initialize__(self, occurrence : Initialize, _event_handlers : list[Callable[[Initialize],None]]):
        it = occurrence
        _event_handlers.append(self._onInitialize)

    def _onInitialize(self, occurrence : Initialize = None) :
        print("Hello World 2")
        # Call the function killMe defined in the capacity Lifecycle
        #self.killMe()
    
    def _onDestroy(self)-> None :
        
        pass
    
    def _receive(self)-> None :
        
        pass
    
    def _inSpace(self, space: Space)-> None :
        
        self.__space = space
    
    def _leave(self)-> None :
        
        pass

