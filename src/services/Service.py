# abstract class Service.

from abc import ABC, abstractmethod
import threading
import asyncio
from enum import Enum
from typing import Optional, Union

"""_summary_ : Enum to define the state of a service.
"""
class ServiceState(Enum) :
    
    CREATED = "CREATED"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"

"""_summary_ : Service base class.
"""
class Service(ABC):
    
    # Constructor.
    def __init__(self, name: Optional[str] = None):
        
        self._name = name if name is not None else self.__class__.__name__
        self._state = ServiceState.CREATED
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None
    
    @property
    def name(self) -> str :
        return self._name
    
    @property
    def state(self) -> ServiceState :
        with self._lock :
            if isinstance(self._state, str) :
                try :
                    return ServiceState(self._state)
                except ValueError :
                    return ServiceState.FAILED
            return self._state
    
    def _set_state(self, new_state: Union[ServiceState, str]) :
        
        with self._lock :
            
            if isinstance(new_state, str) :
                try : self._state = ServiceState(new_state)
                except ValueError : self._state = ServiceState.FAILED
            else :
                self._state = new_state
    
    @abstractmethod
    async def startAsync(self) -> None :
        """Start the service asynchronously."""
        pass
    
    @abstractmethod
    async def stopAsync(self) -> None :
        """Stop the service asynchronously."""
        pass
    
    async def awaitRunning(self) -> None :
        """Wait until the service is in a RUNNING state (without blocking the loop)."""
        while self.state != ServiceState.RUNNING :
            
            if self.state in [ServiceState.STOPPED, ServiceState.FAILED] :
                
                raise RuntimeError("Service " + self._name + " stopped or failed")
            
            await asyncio.sleep(0.1)
    
    async def start_async(self) :
        
        self._thread = threading.Thread(daemon=True)
        await self.startAsync()
    
    async def stop_async(self) :
        
        await self.stopAsync()