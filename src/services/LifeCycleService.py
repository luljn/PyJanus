# services/LifeCycleService.py – FINAL VERSION with directory unregistration print

from typing import Dict, Optional, Any, Callable, TYPE_CHECKING
import asyncio
from importlib import import_module
import threading

from .Service import Service, ServiceState
from agent.Agent import Agent
from agent.AgentState import AgentState
from event.Event import Event
from space.Space import Space

if TYPE_CHECKING:
    from kernel.Kernel import Kernel


class LifeCycleService(Service):
    
    def __init__(self, agent_concrete_class: Optional[Agent] = None):
        super().__init__()
        self._agents: Dict[str, Agent] = {}
        self._agent_ids: Dict[Any, str] = {}
        self._behaviors: Dict[str, Any] = {}
        self._agent_concrete_class = agent_concrete_class
        self._lock = threading.Lock()
        self._running = False
        self._callbacks: Dict[str, list] = {}
    
    async def startAsync(self) -> None:
        self._set_state("STARTING")
        self._running = True
        self._set_state(ServiceState.RUNNING)
        print(f"[{self.name}] Service started.")
    
    async def stopAsync(self) -> None:
        self._set_state("STOPPING")
        self._running = False
        print(f"[{self.name}] Service stopping")
        with self._lock:
            agent_ids = list(self._agents.keys())
            for agent_id in agent_ids:
                await self._kill_agent_async(agent_id, auto_destroy=True)
        self._set_state(ServiceState.STOPPED)
        print(f"[{self.name}] Service stopped")
    
    # ---------- Helper methods ----------
    def _add_agent(self, agent: Agent) -> None:
        agent_id = str(agent.getID())
        with self._lock:
            self._agents[agent_id] = agent
            self._agent_ids[agent] = agent_id
    
    def _remove_agent(self, agent_id: str) -> Optional[Agent]:
        with self._lock:
            agent = self._agents.pop(agent_id, None)
            if agent:
                self._agent_ids.pop(agent, None)
            return agent
    
    def _call_agent_method(self, agent, private_method_name: str, fallback_name: str, *args, **kwargs):
        if hasattr(agent, private_method_name):
            return getattr(agent, private_method_name)(*args, **kwargs)
        if hasattr(agent, fallback_name):
            return getattr(agent, fallback_name)(*args, **kwargs)
        raise AttributeError(f"[{self.name}] Agent {agent.__class__.__name__} has neither {private_method_name} nor {fallback_name}")
    
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
        for attr in [f"_{class_name}__{attr_name}", f"_Agent__{attr_name}", attr_name]:
            if hasattr(agent, attr):
                setattr(agent, attr, value)
                return True
        setattr(agent, attr_name, value)
        return True
    
    # ---------- Spawning an agent ----------
    async def spawnAgent(self, name: Optional[str] = None, space: Space = None,
                         agent_class: str = None, auto_initialize: bool = True, **kwargs) -> None:
        if not self._running:
            raise RuntimeError(f"[{self.name}] Service is not in RUNNING state")
        
        # Import the agent class
        try:
            module = import_module(agent_class)
        except ImportError as e:
            raise RuntimeError(f"[{self.name}] Cannot import module '{agent_class}': {e}")
        
        class_name = agent_class.split('.')[-1]
        agent_class_to_use = getattr(module, class_name, None)
        if agent_class_to_use is None:
            raise RuntimeError(f"[{self.name}] Class '{class_name}' not found in module '{agent_class}'")
        if not isinstance(agent_class_to_use, type):
            raise RuntimeError(f"[{self.name}] '{class_name}' is not a class (got {type(agent_class_to_use)})")
        
        try:
            agent: Agent = agent_class_to_use()
            Initialize.initialize(agent)   # sets state to INITIALIZING
        except TypeError as e:
            raise RuntimeError(f"[{self.name}] Instantiation failed {agent_class_to_use}: {e}")
        
        # Apply optional name/space
        if name:
            self._set_agent_attr(agent, 'name', name)
        if space:
            self._set_agent_attr(agent, 'space', space)
        
        # Register the agent in the default space BEFORE _onInitialize
        if not name and not space:
            from kernel.Kernel import Kernel
            default_space = Kernel.getInstance().getDefaultSpace()
            agent.register(default_space)   # this adds agent to space participants
        
        # Add to this service's internal registry
        self._add_agent(agent)
        
        # Now call the agent's initialization method
        if auto_initialize:
            self._call_agent_method(agent, '_onInitialize', 'onInitialize')
        
        # Finally, emit AgentSpawned event (now the agent is already in the space)
        self.emitAgentSpawned(agent)
        
        print(f"\n[{self.name}] Agent spawned -> Name: {agent.getName()} - ID: {agent.getID()} - Type: {agent.__class__.__name__}\n")
    
    # ---------- Killing an agent ----------
    async def killAgent(self, agent_id: str, auto_destroy: bool = True) -> bool:
        if not self._running:
            return False
        return await self._kill_agent_async(agent_id, auto_destroy)
    
    async def _kill_agent_async(self, agent_id: str, auto_destroy: bool = True) -> bool:
        agent = None
        with self._lock:
            if agent_id not in self._agents:
                return False
            agent = self._agents[agent_id]
        
        # 1. Unregister from DirectoryService
        from kernel.Kernel import Kernel
        from services.DirectoryService import DirectoryService
        dir_svc = Kernel.getInstance().getService(DirectoryService)
        if dir_svc and dir_svc.HasAgent(agent):
            dir_svc.unregister_agent(agent_id)
            # ADDED: print confirmation (as requested)
            print(f"[DIRECTORY] Unregistered agent {agent.getName()} (ID: {agent_id})")
        
        # 2. Remove from its Space
        space = self._get_agent_attr(agent, 'space', None)
        if space and hasattr(space, 'removeParticipant'):
            space.removeParticipant(agent)
            print(f"[SPACE] Removed {agent.getName()} from {space.getName()}")
        
        # 3. Call agent's destroy hook
        if auto_destroy:
            try:
                self._call_agent_method(agent, '_onDestroy', 'onDestroy')
                print(f"[{self.name}] Called _onDestroy for {agent.getName()}")
            except AttributeError:
                print(f"[{self.name}] Warning: agent {agent.getName()} has no _onDestroy method")
        
        # 4. Remove from behaviors
        if agent_id in self._behaviors:
            behavior = self._behaviors[agent_id]
            if hasattr(behavior, 'onStop'):
                try:
                    behavior.onStop()
                except Exception as e:
                    print(f"Error stopping behavior: {e}")
            del self._behaviors[agent_id]
        
        # 5. Remove from internal maps
        self._remove_agent(agent_id)
        
        print(f"[{self.name}] Agent Killed: {agent.getName()} (ID: {agent_id})")
        return True
    
    # ---------- Other methods ----------
    def getAgent(self, agent_id: str) -> Optional[Agent]:
        with self._lock:
            return self._agents.get(agent_id)
    
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
    
    def emitAgentSpawned(self, agent: Agent) -> Optional[Event]:
        from kernel.Kernel import Kernel
        from services.EventService import EventService
        event_svc = Kernel.getInstance().getService(EventService)
        if event_svc and event_svc.state == ServiceState.RUNNING:
            return event_svc.emit(event_type='event.AgentSpawned',
                                  source=str(agent.getID()),
                                  data=f"Agent {agent.getName()} spawned")
        else:
            print(f"[{self.name}] EventService not ready (state={event_svc.state if event_svc else None})")
            return None


class Initialize:
    @staticmethod
    def initialize(agent: Agent) -> None:
        print(f"Initialization of agent {agent.getName()}")
        agent.setState(AgentState.INITIALIZING)