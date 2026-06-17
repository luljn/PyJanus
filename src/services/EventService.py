# Event service.

import asyncio
from typing import Any, Optional

from .Service import Service
from agent.Agent import Agent
from event.Event import Event
from space.Space import Space

"""_summary_: Manages space(s) and events.
"""
class EventService(Service) :
    
    # Constructor.
    def __init__(self) :
        
        super().__init__()
        self._event_queue: Optional[asyncio.Queue] = None
        self._running = False
    
    # To start the service.
    async def startAsync(self) -> None :
        
        self._set_state("STARTING")
        self._running = True
        self._event_queue = asyncio.Queue()
        self._set_state("RUNNING")
        print("[" + self.name + "] Service started.")
    
    # To stop the service.
    async def stopAsync(self) -> None :
        
        self._set_state("STOPPING")
        self._running = False
        self._set_state("STOPPED")
        print("[" + self.name + "] Service stopped")
    
    # To emit an event in a space.
    def emit(self, event:Event, source:Any = None, data:Any = None, space:Space = None) -> None :
        """Emits an event thread-safely and asynchronously."""
        from kernel.Kernel import Kernel
        
        if source is not None : event.setSource(source)
        if data is not None : event.setData(data)
        
        print(event)
        if space is None : space = Kernel.getInstance().getDefaultSpace() 
        space.send(event)
    
    # To register an agent in a space.
    def registerAgent(self, agent: Agent, space: Space) -> bool :
        
        if agent in space.getParticipants() : return False
        space.addParticipant(agent)
        agent.setSpace(space)
        print("Agent " + agent.getName() + " registered to space " + space.getName() + "\n")
        return True
    
    # To unregister an agent from a space.
    def unregisterAgentFromSpace(self, agent: Agent, space: Space)->bool :
        
        if not (agent in space.getParticipants()) : return False
        space.unregister(agent)
        agent.setSpace(None)
        print("Agent " + agent.getName() + " unregistered from space " + space.getName() + "\n")
        return True
    
    # To process the reception on an event.
    def receive(self, agent: Agent, event: Event)->None :
        
        print("[" + agent.getName() + "] received the event Event_" + str(event.getID()) + "\ndata : " + str(event.getData()) + "\n")