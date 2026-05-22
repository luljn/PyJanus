# Event Service

from .Service import Service
from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio
import uuid

@dataclass
class Event:
    """Structure d'un événement"""
    id: str
    event_type: str
    source: str
    data: Any
    timestamp: datetime
    
    def getSource(self) -> str:
        return self.source
    
    def setSource(self, source: str) -> None:
        self.source = source
    
    def toString(self) -> str:
        return f"Event(id={self.id}, type={self.event_type}, source={self.source})"

class EventListener:
    """Écouteur d'événements"""
    def __init__(self, listener_id: str, event_type: str, callback: Callable, owner: str):
        self.id = listener_id
        self.event_type = event_type
        self.callback = callback
        self.owner = owner
    
    async def execute(self, event: Event) -> None:
        """Exécute le callback avec l'événement"""
        if asyncio.inspect.iscoroutinefunction(self.callback):
            await self.callback(event)
        else:
            self.callback(event)

class EventService(Service):
    
    def __init__(self):
        super().__init__()
        self._listeners: Dict[str, List[EventListener]] = {}  # event_type -> list of listeners
        self._event_queue: asyncio.Queue = asyncio.Queue()
        self._dispatcher_task: Optional[asyncio.Task] = None
        self._running = False
    
    def startAsync(self) -> None:
        """Démarre le service d'événements"""
        self._set_state("STARTING")
        self._running = True
        # Créer et démarrer le dispatcher dans un thread ou loop
        self._dispatcher_task = asyncio.create_task(self._dispatch_loop())
        self._set_state("RUNNING")
    
    def stopAsync(self) -> None:
        """Arrête le service d'événements"""
        self._set_state("STOPPING")
        self._running = False
        
        if self._dispatcher_task:
            self._dispatcher_task.cancel()
        
        self._set_state("STOPPED")
    
    def awaitRunning(self) -> None:
        """Attend que le service soit en état RUNNING"""
        while self._state != "RUNNING":
            if self._state in ["STOPPED", "FAILED"]:
                raise RuntimeError("EventService stopped or failed")
            import time
            time.sleep(0.1)
    
    def registerListener(self, event_type: str, callback: Callable, owner: str) -> str:
        """Enregistre un écouteur pour un type d'événement"""
        listener_id = str(uuid.uuid4())
        listener = EventListener(listener_id, event_type, callback, owner)
        
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        
        self._listeners[event_type].append(listener)
        return listener_id
    
    def unregisterListener(self, listener_id: str) -> bool:
        """Désenregistre un écouteur par son ID"""
        for event_type, listeners in self._listeners.items():
            for i, listener in enumerate(listeners):
                if listener.id == listener_id:
                    listeners.pop(i)
                    if not listeners:
                        del self._listeners[event_type]
                    return True
        return False
    
    def unregisterListenerByOwner(self, owner: str) -> int:
        """Désenregistre tous les écouteurs d'un propriétaire"""
        count = 0
        for event_type in list(self._listeners.keys()):
            initial_count = len(self._listeners[event_type])
            self._listeners[event_type] = [
                l for l in self._listeners[event_type] 
                if l.owner != owner
            ]
            removed = initial_count - len(self._listeners[event_type])
            count += removed
            
            if not self._listeners[event_type]:
                del self._listeners[event_type]
        return count
    
    def emit(self, event_type: str, source: str, data: Any = None) -> str:
        """Émet un événement (synchrone, pour être appelé depuis n'importe où)"""
        event = Event(
            id=str(uuid.uuid4()),
            event_type=event_type,
            source=source,
            data=data,
            timestamp=datetime.now()
        )
        
        # Ajouter à la queue asynchrone
        asyncio.create_task(self._queue_event(event))
        return event.id
    
    async def _queue_event(self, event: Event) -> None:
        """Ajoute un événement à la queue"""
        await self._event_queue.put(event)
    
    async def _dispatch_loop(self) -> None:
        """Boucle de distribution des événements"""
        while self._running:
            try:
                event = await asyncio.wait_for(self._event_queue.get(), timeout=0.5)
                await self._dispatch_event(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Erreur dans le dispatch des événements: {e}")
    
    async def _dispatch_event(self, event: Event) -> None:
        """Distribue un événement à tous ses écouteurs"""
        listeners = self._listeners.get(event.event_type, [])
        
        if not listeners:
            return
        
        tasks = []
        for listener in listeners:
            tasks.append(self._safe_execute_listener(listener, event))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _safe_execute_listener(self, listener: EventListener, event: Event) -> None:
        """Exécute un écouteur de façon sécurisée"""
        try:
            await listener.execute(event)
        except Exception as e:
            print(f"Erreur dans l'écouteur {listener.id}: {e}")
    
    def getListenerCount(self, event_type: str = None) -> int:
        """Retourne le nombre d'écouteurs"""
        if event_type:
            return len(self._listeners.get(event_type, []))
        else:
            return sum(len(listeners) for listeners in self._listeners.values())