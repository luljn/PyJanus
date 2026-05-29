# abstract class Agent

from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from .AgentState import AgentState
from space.Space import Space

class Agent(ABC) :
    
    @abstractmethod
    def __init__(self) :
        
        self.__id: UUID = uuid4()
        self.__name: str = f"Agent_{self.__id}"
        self.__state: AgentState = AgentState.NOT_RUNNING
        self.__space: Space = None
    
    @abstractmethod
    def __onInitialize(self)-> None :
        
        raise NotImplementedError("Not implemented !")
    
    @abstractmethod
    def __onDestroy(self)-> None :
        
        raise NotImplementedError("Not implemented !")
    
    @abstractmethod
    def __receive(self)-> None :
        
        raise NotImplementedError("Not implemented !")
    
    @abstractmethod
    def __inSpace(self, space: Space)-> None :
        
        self.__space = space
    
    @abstractmethod
    def __leave(self)-> None :
        
        raise NotImplementedError("Not implemented !")
