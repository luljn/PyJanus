###

from abc import ABC, abstractmethod
from uuid import UUID

from .AgentState import AgentState

class Agent(ABC) : 
    
    @abstractmethod
    def __init__(self, id: UUID, name: str) :
        
        self.id: UUID = id
        self.name: str = name
        self.state: AgentState = AgentState.NOT_RUNNING
        self.space = None
    
    @abstractmethod
    def onInitialize(self)-> None :
        
        raise NotImplementedError("Not implemented !")
    
    @abstractmethod
    def onDestroy(self)-> None :
        
        raise NotImplementedError("Not implemented !")
    
    @abstractmethod
    def receive(self)-> None :
        
        raise NotImplementedError("Not implemented !")
    
    @abstractmethod
    def inSpace(self)-> None :
        
        raise NotImplementedError("Not implemented !")
    
    @abstractmethod
    def leave(self)-> None :
        
        raise NotImplementedError("Not implemented !")
