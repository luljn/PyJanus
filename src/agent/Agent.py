# abstract class Agent

from __future__ import annotations
from abc import ABC, abstractmethod
from asyncio import create_task
from uuid import UUID, uuid4
from threading import Thread
from typing import TYPE_CHECKING, Type, Optional

from .AgentState import AgentState
from event.Event import Event
if TYPE_CHECKING :
    from services.LifeCycleService import Initialize
    from skills.Skill import Skill
    from space.Space import Space

class Agent(ABC) :
    
    # Constructor.
    def __init__(self, id: UUID = None) :
        
        self.__id: UUID = uuid4() if id is None else id
        self.__name: str = f"{self.__class__.__name__}_{self.__id}"
        self.__state: AgentState = AgentState.NOT_RUNNING
        self.__thread: Thread = None
        self.__space: Optional[Space] = None
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
        
        self.setState(AgentState.DESTROYING)
        print(f"[{self.getName()}] Agent destroyed\n")
    
    def _receive(self, event:Event)-> None :
        
        print(f"[{self.getName()}] received the event Event_{event.getID()}\ndata : {event.getData()}\n")
    
    def _inSpace(self, space: Space)-> bool :
        
        if self in space.getParticipants() : return True
        return False
    
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
    
    # To emit an event.
    def emit(self, eventType:Event)->None :
        from capacities.EventCapacity import EventCapacity
        EventCapacity.emitEvent(self, eventType)
    
    # To request the death.
    def killMe(self) :
        from capacities.LifeCycleCapacity import LifeCycleCapacity
        LifeCycleCapacity.killMe(self)
    
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
    
    def setSpace(self, space: Optional[Space])-> None :
        
        self.__space = space
