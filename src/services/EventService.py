import asyncio
from importlib import import_module
from typing import Dict, List, Callable, Any, Optional
from uuid import UUID, uuid4

from .Service import Service
from agent.Agent import Agent
from event.Event import Event
from space.Space import Space



class EventListener :
    
    def __init__(self, listener_id: str, event_type: str, callback: Callable, owner: str):
        self.id = listener_id
        self.event_type = event_type
        self.callback = callback
        self.owner = owner
    
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
        
        super().__init__()
        self._listeners: Dict[str, List[EventListener]] = {}
        self._event_queue: Optional[asyncio.Queue] = None
        self._dispatcher_task: Optional[asyncio.Task] = None
        self._running = False
    
    async def startAsync(self) -> None :
        
        self._set_state("STARTING")
        self._running = True
        self._event_queue = asyncio.Queue()
        self._dispatcher_task = asyncio.create_task(self._dispatch_loop())
        self._set_state("RUNNING")
        print(f"[{self.name}] Service started.")
    
    async def stopAsync(self) -> None :
        
        self._set_state("STOPPING")
        self._running = False
        if self._dispatcher_task:
            self._dispatcher_task.cancel()
            try:
                await self._dispatcher_task
            except asyncio.CancelledError:
                pass
        self._set_state("STOPPED")
        print(f"[{self.name}] Service stoped")
    
    def registerListener(self, event_type: str, callback: Callable, owner: str) -> str :
        
        listener_id = str(uuid4())
        listener = EventListener(listener_id, event_type, callback, owner)
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)
        return listener_id
    
    def unregisterListener(self, listener_id: str) -> bool :
        
        for event_type, listeners in self._listeners.items():
            for i, listener in enumerate(listeners):
                if listener.id == listener_id:
                    listeners.pop(i)
                    if not listeners:
                        del self._listeners[event_type]
                    return True
        return False
    
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
    def emit(self, event:Event, source:Any = None, data:Any = None) -> Event :
        """Emits an event thread-safely and asynchronously."""
        from kernel.Kernel import Kernel
        """event_class_to_use = getattr(import_module(event_type), event_type.split('.')[-1])
        event:Event = event_class_to_use(source=source,data=data) """
        
        if source is not None : event.setSource(source)
        if data is not None : event.setData(data)
        
        if self._running and self._event_queue is not None:
            # Allows inserting from any original asynchronous thread or loop
            try:
                loop = asyncio.get_running_loop()
                loop.call_soon_threadsafe(self._event_queue.put_nowait, event)
                #if(source is not None and issubclass(source, Agent)) : source.getSpace().emit()
            except RuntimeError:
                # If no loop is active in the current thread
                if self._loop and self._loop.is_running():
                    self._loop.call_soon_threadsafe(self._event_queue.put_nowait, event)
        Kernel.getInstance().getDefaultSpace().send(event)
        #return event
        
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
                print(f"Erreur dans la boucle du dispatcher d'événements: {e}")
    
    # To register an agent in a space.
    def registerAgent(self, agent: Agent, space: Space) -> bool :
        
        if agent in space.getParticipants() : return False
        space.addParticipant(agent)
        agent.setSpace(space)
        print(f"Agent {agent.getName()} registered to space {space.getName()}\n")
        return True