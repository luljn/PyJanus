from abc import ABC, abstractmethod
import threading
import asyncio
from enum import Enum
from time import sleep
from typing import Optional, Union

class ServiceState(Enum):
    CREATED = "CREATED"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"

class Service(ABC):
    """Classe abstraite de base tolérante et robuste pour tous les services du système SARL"""
    
    def __init__(self, name: Optional[str] = None):
        self._name = name if name is not None else self.__class__.__name__
        self._state = ServiceState.CREATED
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def state(self) -> ServiceState:
        with self._lock:
            if isinstance(self._state, str):
                try:
                    return ServiceState(self._state)
                except ValueError:
                    return ServiceState.FAILED
            return self._state
    
    def _set_state(self, new_state: Union[ServiceState, str]):
        with self._lock:
            if isinstance(new_state, str):
                try:
                    self._state = ServiceState(new_state)
                except ValueError:
                    self._state = ServiceState.FAILED
            else:
                self._state = new_state
    
    @abstractmethod
    async def startAsync(self) -> None:
        """Démarre le service de façon asynchrone"""
        pass
    
    @abstractmethod
    async def stopAsync(self) -> None:
        """Arrête le service de façon asynchrone"""
        pass
    
    async def awaitRunning(self) -> None:
        """Attend que le service soit en état RUNNING (sans bloquer la boucle)"""
        while self.state != ServiceState.RUNNING:
            if self.state in [ServiceState.STOPPED, ServiceState.FAILED]:
                raise RuntimeError(f"Service {self._name} stopped or failed")
            await asyncio.sleep(0.1)
    
    def start_async_threaded(self) -> None:
        """Démarre le service dans un thread séparé"""
        if self._thread and self._thread.is_alive():
            raise RuntimeError(f"Service {self._name} already running")
        
        self._thread = threading.Thread(target=self._run_async_loop, daemon=True)
        self._thread.start()
    
    def _run_async_loop(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self.startAsync())
    
    def stop_threaded(self):
        """Arrête le service de façon threadée"""
        if self._loop:
            asyncio.run_coroutine_threadsafe(self.stopAsync(), self._loop)
    
    async def start_async(self):
        #self._thread = threading.Thread(target=sleep(1), daemon=True)
        self._thread = threading.Thread(daemon=True)
        await self.startAsync()
    
    async def stop_async(self):
        await self.stopAsync()