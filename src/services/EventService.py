import asyncio
import threading
from importlib import import_module
from typing import Dict, List, Callable, Any, Optional
from uuid import uuid4

from .Service import Service, ServiceState
from agent.Agent import Agent
from event.Event import Event
from space.Space import Space


class EventListener:
    def __init__(self, listener_id: str, event_type: str, callback: Callable, owner: str):
        self.id = listener_id
        self.event_type = event_type
        self.callback = callback
        self.owner = owner

    async def execute(self, event: Event) -> None:
        try:
            if asyncio.iscoroutinefunction(self.callback):
                await self.callback(event)
            else:
                self.callback(event)
        except Exception as e:
            print(f"Error in listener {self.id} from {self.owner}: {e}")


class EventService(Service):
    def __init__(self):
        super().__init__()
        self._listeners: Dict[str, List[EventListener]] = {}
        self._event_queue: Optional[asyncio.Queue] = None
        self._dispatcher_task: Optional[asyncio.Task] = None
        self._running = False
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None

    async def startAsync(self) -> None:
        # No-op for compatibility; use start() instead
        pass

    def start(self) -> None:
        if self._running:
            return
        self._set_state("STARTING")
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        import time
        time.sleep(0.1)
        self._set_state(ServiceState.RUNNING)
        print(f"[{self.name}] Service started in background thread.")

    def _run_loop(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._event_queue = asyncio.Queue()
        self._dispatcher_task = self._loop.create_task(self._dispatch_loop())
        self._loop.run_forever()

    async def stopAsync(self) -> None:
        self._set_state("STOPPING")
        self._running = False
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        self._set_state(ServiceState.STOPPED)
        print(f"[{self.name}] Service stopped.")

    def registerListener(self, event_type: str, callback: Callable, owner: str) -> str:
        listener_id = str(uuid4())
        listener = EventListener(listener_id, event_type, callback, owner)
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)
        print(f"[EVENT_SERVICE] Registered listener for {event_type} from {owner}")
        return listener_id

    def unregisterListener(self, listener_id: str) -> bool:
        for event_type, listeners in self._listeners.items():
            for i, l in enumerate(listeners):
                if l.id == listener_id:
                    listeners.pop(i)
                    if not listeners:
                        del self._listeners[event_type]
                    return True
        return False

    def unregisterListenerByOwner(self, owner: str) -> int:
        count = 0
        for event_type in list(self._listeners.keys()):
            initial = len(self._listeners[event_type])
            self._listeners[event_type] = [l for l in self._listeners[event_type] if l.owner != owner]
            count += initial - len(self._listeners[event_type])
            if not self._listeners[event_type]:
                del self._listeners[event_type]
        return count

    # Emit an event by type string (creates a new instance) – used for AgentSpawned
    def emit(self, event_type: str, source: str = None, data: Any = None) -> Event:
        print(f"[EVENT_SERVICE] emit called with {event_type}, source={source}")
        try:
            module = import_module(event_type)
            class_name = event_type.split('.')[-1]
            event_class = getattr(module, class_name)
        except (ImportError, AttributeError):
            parts = event_type.rsplit('.', 1)
            if len(parts) != 2:
                raise ValueError(f"Invalid event_type: {event_type}")
            module_path, class_name = parts
            module = import_module(module_path)
            event_class = getattr(module, class_name)

        event = event_class()
        event.event_type = event_type
        if source:
            event.setSource(source)
        event.data = data

        if self._running and self._event_queue is not None:
            if self._loop:
                self._loop.call_soon_threadsafe(self._event_queue.put_nowait, event)
                print(f"[EVENT_SERVICE] Queued event {event_type}")
        return event

    # Emit an already constructed event (preserves custom fields)
    def emit_event(self, event: Event) -> None:
        if not self._running or self._event_queue is None:
            print(f"[EVENT_SERVICE] Cannot emit event, service not running")
            return
        if self._loop:
            self._loop.call_soon_threadsafe(self._event_queue.put_nowait, event)
            print(f"[EVENT_SERVICE] Queued event {event.event_type} from existing instance")
        else:
            print(f"[EVENT_SERVICE] No event loop available")

    async def _dispatch_loop(self) -> None:
        while self._running:
            try:
                event = await self._event_queue.get()
                print(f"[EVENT_SERVICE] Dispatching event {event.event_type}")
                listeners = self._listeners.get(event.event_type, []).copy()
                for listener in listeners:
                    asyncio.create_task(listener.execute(event))
                self._event_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in event dispatcher: {e}")

    def registerAgent(self, agent: Agent, space: Space) -> bool:
        if agent in space.getParticipants():
            return False
        space.addParticipant(agent)
        print(f"Agent {agent.getName()} registered to space {space.getName()}")
        return True