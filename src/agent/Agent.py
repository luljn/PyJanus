# Abstract class Agent.

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

"""_summary_ : The base class for all the agents.
"""
class Agent(ABC) :
    
    # Constructor.
    def __init__(self, id: UUID = None) :
        
        self.__id: UUID = uuid4() if id is None else id
        self.__name: str = self.__class__.__name__ + "_" + str(self.__id)
        self.__state: AgentState = AgentState.NOT_RUNNING
        self.__thread: Thread = None
        self.__space: Optional[Space] = None
        self.__skills:list[Skill] = []
        
        # Adding skills to the skills list.
        from skills.EventSkill import EventSkill
        from skills.KillSkill import KillSkill
        from skills.SpawnSkill import SpawnSkill
        self.__skills.extend([EventSkill(), KillSkill(), SpawnSkill()])
    
    # Initialization method.
    @abstractmethod
    def _onInitialize(self, occurrence : Initialize = None) :
        
        self.__thread = Thread(daemon=True)
        self.__thread.start()
    
    # Destruction method.
    @abstractmethod
    def _onDestroy(self)-> None :
        
        self.setState(AgentState.DESTROYING)
        print("[" + self.getName() + "] Agent destroyed\n")
    
    # To process the reception of an event.
    def _receive(self, event:Event)-> None :
        
        from capacities.EventCapacity import EventCapacity
        EventCapacity.receive(self, event)
    
    # To determine if an agent is a participant of a specific space.
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
        print("[" + self.__name + "] agent to spawn : " + agentType)
        create_task(LifeCycleCapacity.spawn(self, agentType))
    
    # To emit an event.
    def emit(self, eventType:Event)->None :
        from capacities.EventCapacity import EventCapacity
        EventCapacity.emitEvent(self, eventType)
    
    # To request the death.
    def killMe(self) :
        from capacities.LifeCycleCapacity import LifeCycleCapacity
        create_task(LifeCycleCapacity.killMe(self))
    
    # Getters.
    def getID(self) -> int :
        
        return self.__id
    
    def getName(self) -> str :
        
        return self.__name
    
    def getState(self) -> AgentState :
        
        return self.__state
    
    def getSpace(self) -> Space :
        
        return self.__space
    
    # Setters.
    def setName(self, name: str)-> None :
        
        self.__name = name
    
    def setState(self, state: AgentState)-> None :
        
        self.__state = state
    
    def setSpace(self, space: Optional[Space])-> None :
        
        self.__space = space
