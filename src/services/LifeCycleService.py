# LifeCycleService

from typing import Dict, Optional, Any, Callable, TYPE_CHECKING, Type
import uuid
import asyncio
from importlib import import_module
import threading

from .Service import Service
from agent.Agent import Agent
from agent.AgentState import AgentState
from behavior.Behavior import Behavior
from event.Event import Event
from space.Space import Space
if TYPE_CHECKING :
    from kernel.Kernel import Kernel
    from services.EventService import EventService


class LifeCycleService(Service):
    
    def __init__(self, agent_concrete_class: Optional[Agent] = None):
        """Initialize the LifeCycleService."""
        super().__init__()
        self._agents: Dict[str, Agent] = {}          # ID externe -> agent
        self._agent_ids: Dict[Any, str] = {}       # agent -> ID externe
        self._behaviors: Dict[str, Any] = {}       # ID agent -> behavior
        self._agent_concrete_class = agent_concrete_class
        self._lock = threading.Lock()
        self._running = False
        self._callbacks: Dict[str, list] = {}
    
    async def startAsync(self) -> None:
        self._set_state("STARTING")
        self._running = True
        #self._thread = threading.Thread(daemon=True)
        self._thread.start()
        self._set_state("RUNNING")
        print(f"[{self.name}] Service started.")
    
    async def stopAsync(self) -> None:
        self._set_state("STOPPING")
        self._running = False
        print(f"[{self.name}] Service stoped")
        
        with self._lock:
            agent_ids = list(self._agents.keys())
            for agent_id in agent_ids:
                await self._kill_agent_async(agent_id)
        
        self._set_state("STOPPED")
        print(f"[{self.name}] Service stopped")
    
    def _call_agent_method(self, agent, private_method_name: str, fallback_name: str, *args, **kwargs):
        """Dynamically calls a method of the agent (protected or public)."""
        class_name = agent.__class__.__name__
        
        # 1. Try with the protected name (ex: '_onInitialize')
        if hasattr(agent, private_method_name):
            return getattr(agent, private_method_name)(*args, **kwargs)
            
        # 2. Fallback on the alternative public method (ex: 'onInitialize')
        if hasattr(agent, fallback_name):
            return getattr(agent, fallback_name)(*args, **kwargs)
            
        # 3. If no one exists
        raise AttributeError(f"[{self.name}] L'agent {class_name} n'a ni la méthode {private_method_name}, ni {fallback_name}")
    
    def _get_agent_attr(self, agent, attr_name: str, default=None):
        class_name = agent.__class__.__name__
        mangled_attr = f"_{class_name}__{attr_name}"
        if hasattr(agent, mangled_attr):
            return getattr(agent, mangled_attr)
        
        mangled_base = f"_Agent__{attr_name}"
        if hasattr(agent, mangled_base):
            return getattr(agent, mangled_base)
            
        if hasattr(agent, attr_name):
            return getattr(agent, attr_name)
        return default
    
    def _set_agent_attr(self, agent, attr_name: str, value) -> bool:
        class_name = agent.__class__.__name__
        mangled_attrs = [f"_{class_name}__{attr_name}", f"_Agent__{attr_name}", attr_name]
        
        for attr in mangled_attrs:
            if hasattr(agent, attr):
                setattr(agent, attr, value)
                return True
        setattr(agent, attr_name, value)
        return True
    
    async def spawnAgent(self, name: Optional[str] = None, space:Space=None, agent_class:str=None, 
                         auto_initialize: bool = True, **kwargs) -> None :
        if not self._running:
            raise RuntimeError(f"[{self.name}] Service is not in RUNNING state")
        
        agent_class_to_use = getattr(import_module(agent_class), agent_class.split('.')[-1])
        if not agent_class_to_use:
            raise RuntimeError(f"[{self.name}] No Agent class given.")
        
        try:
            # Agent creation and initialization.
            agent:Agent = agent_class_to_use()
            Initialize.initialize(agent)
        except TypeError as e:
            raise RuntimeError(f"[{self.name}] Instantiation failed {agent_class_to_use}: {e}")
        
        if name:
            self._set_agent_attr(agent, 'name', name)
        if space:
            self._set_agent_attr(agent, 'space', space)
        
        if auto_initialize:
            """ try:
                self._call_agent_method(agent, '_onInitialize', 'onInitialize')
                print(self.emitAgentSpawned(agent))
            except AttributeError:
                print(f"[{self.name}] Warning: agent has not onInitialize method") """
            self._call_agent_method(agent, '_onInitialize', 'onInitialize')
            print(self.emitAgentSpawned(agent))
        
        if (not name and not space) :
            from kernel.Kernel import Kernel
            agent.register(Kernel.getInstance().getDefaultSpace())
            #await self._trigger_callbacks('agent_created', agent.getID(), agent)
        
        print(f"\n[{self.name}] Agent spawned-> Name: {agent.getName()} - ID: {agent.getID()} - Type: {agent.__class__.__name__}\n")
    
    async def killAgent(self, agent_id: str, auto_destroy: bool = True) -> bool:
        if not self._running:
            return False
        return await self._kill_agent_async(agent_id, auto_destroy)
    
    async def _kill_agent_async(self, agent_id: str, auto_destroy: bool = True) -> bool:
        with self._lock:
            if agent_id not in self._agents:
                return False
            agent = self._agents[agent_id]
            
            if auto_destroy:
                try:
                    self._call_agent_method(agent, '_onDestroy', 'onDestroy')
                except AttributeError:
                    print(f"[{self.name}] Warning: agent has not onDestroy method")
            
            if agent_id in self._behaviors:
                behavior = self._behaviors[agent_id]
                if hasattr(behavior, 'onStop'):
                    try: behavior.onStop()
                    except Exception as e: print(f"Error stopping behavior: {e}")
                del self._behaviors[agent_id]
            
            del self._agents[agent_id]
            if agent in self._agent_ids:
                del self._agent_ids[agent]
            
            agent_name = self._get_agent_attr(agent, 'name', "Unknown")
            print(f"[{self.name}] Agent Killed: {agent_name} (ID: {agent_id})")
            return True
            
    def getAgent(self, agent_id: str) -> Optional[Any]:
        with self._lock: return self._agents.get(agent_id)
        
    async def sendMessage(self, to_agent_id: str, message: Any) -> bool:
        with self._lock:
            if to_agent_id not in self._agents:
                return False
            agent = self._agents[to_agent_id]
            
        try:
            self._call_agent_method(agent, '__receive', 'receive', message)
            return True
        except AttributeError:
            print(f"[{self.name}] Warning: No receiving entry point found on the agent")
            return False

    def getAgentName(self, agent_id: str) -> Optional[str]:
        agent = self.getAgent(agent_id)
        return self._get_agent_attr(agent, 'name') if agent else None

    def registerCallback(self, event: str, callback: Callable):
        if event not in self._callbacks:
            self._callbacks[event] = []
        self._callbacks[event].append(callback)
    
    async def _trigger_callbacks(self, event: str, *args, **kwargs):
        if event in self._callbacks:
            for callback in self._callbacks[event]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(*args, **kwargs)
                    else:
                        callback(*args, **kwargs)
                except Exception as e:
                    print(f"[{self.name}] Error in callback {event}: {e}")
    
    # To emit AgentSpawned event.
    def emitAgentSpawned(self, agent:Agent)->Event : 
        from kernel.Kernel import Kernel
        from services.EventService import EventService
        return Kernel.getInstance().getService(EventService).emit(event_type='event.AgentSpawned', source=str(agent.getID()), 
                                                            data=f"Agent {agent.getName()} spawned")

class Initialize:
    """Initialization event for agents"""
    @staticmethod
    def initialize(agent: Agent)-> None : 
        print(f"Initialization of agent {agent.getName()}")
        agent.setState(AgentState.INITIALIZING)
        return None