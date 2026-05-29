# abstract class Agent

from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from .AgentState import AgentState
from space.Space import Space
if TYPE_CHECKING :
    from services.LifeCycleService import Initialize

class Agent(ABC) :
    
    @abstractmethod
    def __init__(self) :
        
        self.__id: UUID = uuid4()
        self.__name: str = f"Agent_{self.__id}"
        self.__state: AgentState = AgentState.NOT_RUNNING
        self.__space: Space = None
    
    # Getters
    def getID(self) -> int :
        
        return self.__id
    
    def getName(self) -> str :
        
        return self.__name
    
    def getState(self) -> AgentState :
        
        return self.__state
    
    def getSpace(self) -> Space :
        
        return self.__space
    
    # Setters
    def setState(self, state: AgentState)-> None :
        
        self.__state = state
    
    def setSpace(self, space: Space)-> None :
        
        self.__space = space
    
    @abstractmethod
    def _onInitialize(self, occurrence : Initialize = None) :
        
        self.__state = AgentState.INITIALIZING
    
    @abstractmethod
    def _onDestroy(self)-> None :
        
        raise NotImplementedError("Not implemented !")
    
    @abstractmethod
    def _receive(self)-> None :
        
        raise NotImplementedError("Not implemented !")
    
    @abstractmethod
    def _inSpace(self, space: Space)-> None :
        
        self.__space = space
    
    @abstractmethod
    def _leave(self)-> None :
        
        raise NotImplementedError("Not implemented !")
