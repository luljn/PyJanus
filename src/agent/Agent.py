# abstract class Agent

from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID, uuid4
from threading import Thread
from typing import TYPE_CHECKING, Type

from .AgentState import AgentState
if TYPE_CHECKING :
    from capacities.EventCapacity import EventCapacity
    from capacities.LifeCycleCapacity import LifeCycleCapacity
    from services.LifeCycleService import Initialize
    from skills.Skill import Skill
    from space.Space import Space

class Agent(ABC) :
    
    @abstractmethod
    def __init__(self, id: UUID = None) :
        
        self.__id: UUID = uuid4() if id is None else id
        self.__name: str = f"{self.__class__.__name__}_{self.__id}"
        self.__state: AgentState = AgentState.NOT_RUNNING
        self.__thread: Thread = None
        self.__space: Space = None
        self.__skills:list[Skill] = []
        
        # Adding skills to the skills list.
        from skills.EventSkill import EventSkill
        from skills.KillSkill import KillSkill
        from skills.SpawnSkill import SpawnSkill
        self.__skills.extend([EventSkill(), KillSkill(), SpawnSkill()])
        
        # 
        print(f"[INFO] Agent {self.__name} created")
    
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
    
    # To get a skill with its Type.
    def getSkill(self, skillClass:Type[Skill])-> Skill :
        for skill in self.__skills : 
            if(isinstance(skill, skillClass)) :
                return skill
    
    # To register in a Space
    def register(self, space: Space)-> None :
        
        from capacities.EventCapacity import EventCapacity
        EventCapacity.registerInSpace(self, space)
    
    @abstractmethod
    def _onInitialize(self, occurrence : Initialize = None) :
        
        #self.__state = AgentState.INITIALIZING
        #raise NotImplementedError("Not implemented !")
        self.__thread = Thread(target=self.test, daemon=True)
        self.__thread.start()
    
    @abstractmethod
    def _onDestroy(self)-> None :
        
        raise NotImplementedError("Not implemented !")
    
    @abstractmethod
    def _receive(self)-> None :
        
        raise NotImplementedError("Not implemented !")
    
    @abstractmethod
    def _inSpace(self, space: Space)-> bool :
        
        raise NotImplementedError("Not implemented !")
    
    @abstractmethod
    def _leave(self)-> None :
        
        raise NotImplementedError("Not implemented !")
    
    #
    def test(self) :
        pass 
