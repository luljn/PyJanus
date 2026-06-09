<<<<<<< HEAD
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio
import uuid
from .Service import Service
@dataclass
class Event:
    """Structure d'un événement au sein du système de communication"""
    id: str
    event_type: str
    source: str
    data: Any
    timestamp: datetime
    
    def getSource(self) -> str: return self.source
    def setSource(self, source: str) -> None: self.source = source
    def toString(self) -> str:
        return f"Event(id={self.id}, type={self.event_type}, source={self.source})"

class EventListener:
=======
import asyncio
from importlib import import_module
from typing import Dict, List, Callable, Any, Optional
from uuid import UUID, uuid4

from .Service import Service
from agent.Agent import Agent
from event.Event import Event
from space.Space import Space



class EventListener :
    
>>>>>>> origin/branch3-thread_management
    def __init__(self, listener_id: str, event_type: str, callback: Callable, owner: str):
        self.id = listener_id
        self.event_type = event_type
        self.callback = callback
        self.owner = owner
<<<<<<< HEAD
    
    async def execute(self, event: Event) -> None:
        try:
            if asyncio.iscoroutinefunction(self.callback):
                await self.callback(event)
            else:
                self.callback(event)
        except Exception as e:
            print(f"Erreur lors de l'exécution de l'écouteur {self.id} de {self.owner}: {e}")

class EventService(Service):
    
    def __init__(self):
=======
    
    async def execute(self, event: Event) -> None :
        try:
            if asyncio.iscoroutinefunction(self.callback):
                await self.callback(event)
            else:
                self.callback(event)
        except Exception as e:
            print(f"Erreur lors de l'exécution de l'écouteur {self.id} de {self.owner}: {e}")

class EventService(Service) :
    
    def __init__(self) :
        
>>>>>>> origin/branch3-thread_management
        super().__init__()
        self._listeners: Dict[str, List[EventListener]] = {}
        self._event_queue: Optional[asyncio.Queue] = None
        self._dispatcher_task: Optional[asyncio.Task] = None
        self._running = False
    
<<<<<<< HEAD
    async def startAsync(self) -> None:
=======
    async def startAsync(self) -> None :
        
>>>>>>> origin/branch3-thread_management
        self._set_state("STARTING")
        self._running = True
        self._event_queue = asyncio.Queue()
        self._dispatcher_task = asyncio.create_task(self._dispatch_loop())
        self._set_state("RUNNING")
<<<<<<< HEAD
        print(f"[{self.name}] Service d'événements prêt.")
    
    async def stopAsync(self) -> None:
=======
        print(f"[{self.name}] Service started.")
    
    async def stopAsync(self) -> None :
        
>>>>>>> origin/branch3-thread_management
        self._set_state("STOPPING")
        self._running = False
        if self._dispatcher_task:
            self._dispatcher_task.cancel()
            try:
                await self._dispatcher_task
            except asyncio.CancelledError:
                pass
        self._set_state("STOPPED")
<<<<<<< HEAD
    
    def registerListener(self, event_type: str, callback: Callable, owner: str) -> str:
        listener_id = str(uuid.uuid4())
=======
        print(f"[{self.name}] Service stoped")
    
    def registerListener(self, event_type: str, callback: Callable, owner: str) -> str :
        
        listener_id = str(uuid4())
>>>>>>> origin/branch3-thread_management
        listener = EventListener(listener_id, event_type, callback, owner)
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)
        return listener_id
    
<<<<<<< HEAD
    def unregisterListener(self, listener_id: str) -> bool:
=======
    def unregisterListener(self, listener_id: str) -> bool :
        
>>>>>>> origin/branch3-thread_management
        for event_type, listeners in self._listeners.items():
            for i, listener in enumerate(listeners):
                if listener.id == listener_id:
                    listeners.pop(i)
                    if not listeners:
                        del self._listeners[event_type]
                    return True
        return False
    
<<<<<<< HEAD
    def unregisterListenerByOwner(self, owner: str) -> int:
        count = 0
        for event_type in list(self._listeners.keys()):
            initial_count = len(self._listeners[event_type])
            self._listeners[event_type] = [l for l in self._listeners[event_type] if l.owner != owner]
            count += (initial_count - len(self._listeners[event_type]))
            if not self._listeners[event_type]:
                del self._listeners[event_type]
        return count
    
    def emit(self, event_type: str, source: str, data: Any = None) -> str:
        """Émet un événement de manière thread-safe et asynchrone."""
        event_id = str(uuid.uuid4())
        event = Event(id=event_id, event_type=event_type, source=source, data=data, timestamp=datetime.now())
        
        if self._running and self._event_queue is not None:
            # Permet d'insérer depuis n'importe quel thread ou boucle asynchrone d'origine
=======
    def unregisterListenerByOwner(self, owner: str) -> int :
        
        count = 0
        for event_type in list(self._listeners.keys()):
            initial_count = len(self._listeners[event_type])
            self._listeners[event_type] = [l for l in self._listeners[event_type] if l.owner != owner]
            count += (initial_count - len(self._listeners[event_type]))
            if not self._listeners[event_type]:
                del self._listeners[event_type]
        return count
    
    # To emit an event
    def emit(self, event_type: str = "event.Event", source: str = None, data: Any = None) -> Event :
        """Emits an event thread-safely and asynchronously."""
        event_class_to_use = getattr(import_module(event_type), event_type.split('.')[-1])
        event:Event = event_class_to_use()
        
        if self._running and self._event_queue is not None:
            # Allows inserting from any original asynchronous thread or loop
>>>>>>> origin/branch3-thread_management
            try:
                loop = asyncio.get_running_loop()
                loop.call_soon_threadsafe(self._event_queue.put_nowait, event)
            except RuntimeError:
<<<<<<< HEAD
                # Si aucune boucle n'est active dans le thread courant
                if self._loop and self._loop.is_running():
                    self._loop.call_soon_threadsafe(self._event_queue.put_nowait, event)
        return event_id
=======
                # If no loop is active in the current thread
                if self._loop and self._loop.is_running():
                    self._loop.call_soon_threadsafe(self._event_queue.put_nowait, event)
        return event
>>>>>>> origin/branch3-thread_management
        
    async def _dispatch_loop(self) -> None:
        """Boucle de routage interne distribuant les événements aux écouteurs enregistrés."""
        while self._running:
            try:
                if self._event_queue is None:
                    await asyncio.sleep(0.1)
                    continue
                event = await self._event_queue.get()
                
                # Récupérer les listeners pour ce type d'événement ou globaux
                listeners = self._listeners.get(event.event_type, []).copy()
                
                # Exécuter chaque callback en tâche de fond pour ne pas bloquer le bus principal
                for listener in listeners:
                    asyncio.create_task(listener.execute(event))
                    
                self._event_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
<<<<<<< HEAD
                print(f"Erreur dans la boucle du dispatcher d'événements: {e}")
=======
                print(f"Erreur dans la boucle du dispatcher d'événements: {e}")
    
    # To register an agent in a space.
    def registerAgent(self, agent: Agent, space: Space) -> bool :
        
        if agent in space.getParticipants() : return False
        space.addParticipant(agent)
        print(f"Agent {agent.getName()} registered to space {space.getName()}")
        return True
>>>>>>> origin/branch3-thread_management
