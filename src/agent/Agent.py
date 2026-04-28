# abstract class Agent

from abc import ABC, abstractmethod
from uuid import UUID

from .AgentState import AgentState
from space.Space import Space

class Agent(ABC) : 
    
    @abstractmethod
    def __init__(self, id: UUID, name: str) :
        
        self.__id: UUID = id
        self.__name: str = name
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
    def __inSpace(self)-> None :
        
        raise NotImplementedError("Not implemented !")
    
    @abstractmethod
    def __leave(self)-> None :
        
        raise NotImplementedError("Not implemented !")
