import asyncio
import threading
from importlib import import_module
from typing import Any, Optional

from .Service import Service, ServiceState
from agent.Agent import Agent
from event.Event import Event
from space.Space import Space


class EventService(Service):
    def __init__(self):
        super().__init__()
        self._running = False
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None

    async def startAsync(self) -> None:
        # No‑op for compatibility; real start is done by start()
        pass

    def start(self) -> None:
        if self._running:
            return
        self._set_state("STARTING")
        self._running = True
        # We keep a background thread with an event loop only for future async tasks
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        import time
        time.sleep(0.1)
        self._set_state(ServiceState.RUNNING)
        print(f"[{self.name}] Service started (space‑forwarding mode).")

    def _run_loop(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        # No dispatcher – we only forward events to the space.
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

    def emit(self, event_type: str, source: str = None, data: Any = None) -> Event:
        """Create an event and forward it to the default space."""
        print(f"[EVENT_SERVICE] emit called with {event_type}, source={source}")
        # Dynamically import event class
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

        from kernel.Kernel import Kernel
        space = Kernel.getInstance().getDefaultSpace()
        print(f"[EVENT_SERVICE] Forwarding event {event.event_type} to space {space.getName()}")
        space.emit(event)
        return event

    def emit_event(self, event: Event) -> None:
        """Forward an already constructed event to the default space."""
        print(f"[EVENT_SERVICE] Forwarding existing event {event.event_type} to space")
        from kernel.Kernel import Kernel
        space = Kernel.getInstance().getDefaultSpace()
        space.emit(event)

    def registerAgent(self, agent: Agent, space: Space) -> bool:
        """Register an agent in a space (used by EventSkill)."""
        if agent in space.getParticipants():
            return False
        space.addParticipant(agent)
        print(f"Agent {agent.getName()} registered to space {space.getName()}")
        return True