import threading
import queue
from typing import Dict, List, Type
from .Service import Service
from Event import Event

class EventService(Service):
    def __init__(self):
        super().__init__()
        self._queue = queue.Queue()
        self._listeners: Dict[Type[Event], List] = {}
        self._lock = threading.Lock()
        self._thread = None
        self._running = False

    def startAsync(self):
        self._running = True
        self._thread = threading.Thread(target=self._dispatchLoop, daemon=True)
        self._thread.start()
        print("[EventService] démarré")

    def stopAsync(self):
        self._running = False
        self._queue.put(None)
        if self._thread:
            self._thread.join(timeout=2)
        print("[EventService] arrêté")

    def awaitRunning(self):
        while not self._running or self._thread is None:
            import time
            time.sleep(0.01)

    def registerListener(self, event_type: Type[Event], agent) -> None:
        with self._lock:
            if event_type not in self._listeners:
                self._listeners[event_type] = []
            self._listeners[event_type].append(agent)

    def unregisterListener(self, event_type: Type[Event], agent) -> None:
        with self._lock:
            if event_type in self._listeners:
                self._listeners[event_type] = [a for a in self._listeners[event_type] if a != agent]

    def emit(self, event: Event) -> None:
        self._queue.put(event)

    def _dispatchLoop(self):
        while self._running:
            try:
                event = self._queue.get(timeout=0.1)
                if event is None:
                    continue
                event_type = type(event)
                with self._lock:
                    listeners = list(self._listeners.get(event_type, []))
                for agent in listeners:
                    if hasattr(agent, 'receive'):
                        agent.receive(event)
            except queue.Empty:
                continue
