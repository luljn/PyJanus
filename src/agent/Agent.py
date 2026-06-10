# abstract class Agent

from __future__ import annotations
from abc import ABC, abstractmethod
from asyncio import create_task
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
    
    @abstractmethod
    def _onInitialize(self, occurrence : Initialize = None) :
        
        self.__thread = Thread(daemon=True)
        self.__thread.start()
    
    @abstractmethod
    def _onDestroy(self)-> None :
        
        raise NotImplementedError("Not implemented !")
    
    def _receive(self)-> None :
        
        raise NotImplementedError("Not implemented !")
    
    def _inSpace(self, space: Space)-> bool :
        
        if self in space.getParticipants() : return True
        return False
    
    def _leave(self, space: Space)-> None :
        
        if self._inSpace(space) : space.leave(self)
    
    # To get a skill with its Type.
    def getSkill(self, skillClass:Type[Skill])-> Skill :
        for skill in self.__skills : 
            if(isinstance(skill, skillClass)) :
                return skill
    
    # To register in a Space.
    def register(self, space: Space)-> None :
        
        from capacities.EventCapacity import EventCapacity
        EventCapacity.registerInSpace(self, space)
    
    # To spawn an agent.
    def spawnAgent(self, agentType:str) :
        
        from capacities.LifeCycleCapacity import LifeCycleCapacity
        print(f"[{self.__name}] agent to spawn : {agentType}")
        create_task(LifeCycleCapacity.spawn(self, agentType))
    
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
