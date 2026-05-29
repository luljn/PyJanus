from typing import Dict, Optional, Any, Callable
import uuid
import asyncio
from importlib import import_module
import threading

from .Service import Service
from agent.Agent import Agent
from behavior.Behavior import Behavior


class LifeCycleService(Service):
    
    def __init__(self, agent_concrete_class: Optional[Agent] = None):
        """Initialise le service de cycle de vie."""
        super().__init__()
        self._agents: Dict[str, Any] = {}          # ID externe -> agent
        self._agent_ids: Dict[Any, str] = {}       # agent -> ID externe
        self._behaviors: Dict[str, Any] = {}       # ID agent -> behavior
        self._agent_concrete_class = agent_concrete_class
        self._lock = threading.Lock()
        self._running = False
        self._callbacks: Dict[str, list] = {}
    
    async def startAsync(self) -> None:
        self._set_state("STARTING")
        self._running = True
        self._set_state("RUNNING")
        print(f"[{self.name}] Service démarré")
    
    async def stopAsync(self) -> None:
        self._set_state("STOPPING")
        self._running = False
        
        with self._lock:
            agent_ids = list(self._agents.keys())
            for agent_id in agent_ids:
                await self._kill_agent_async(agent_id)
        
        self._set_state("STOPPED")
        print(f"[{self.name}] Service arrêté")
    
    def _call_agent_method(self, agent, private_method_name: str, fallback_name: str, *args, **kwargs):
        """Appelle dynamiquement une méthode de l'agent (protégée ou publique)."""
        class_name = agent.__class__.__name__
        
        # 1. Tenter avec le nom protégé exact (ex: '_onInitialize')
        if hasattr(agent, private_method_name):
            return getattr(agent, private_method_name)(*args, **kwargs)
            
        # 2. Fallback sur la méthode publique alternative (ex: 'onInitialize')
        if hasattr(agent, fallback_name):
            return getattr(agent, fallback_name)(*args, **kwargs)
            
        # 3. Si aucune des deux n'existe, on lève une erreur claire
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
    
    async def spawnAgent(self, name: Optional[str] = None, space=None, agent_class=None, 
                         auto_initialize: bool = True, **kwargs) -> None :
        if not self._running:
            raise RuntimeError(f"[{self.name}] Service n'est pas en état RUNNING")
        
        external_id = str(uuid.uuid4())
        #agent_class_to_use = agent_class or self._agent_concrete_class
        agent_class_to_use = getattr(import_module(agent_class), agent_class.split('.')[-1])
        if not agent_class_to_use:
            raise RuntimeError(f"[{self.name}] Aucune classe d'agent fournie.")
        
        try:
            # On instancie l'agent en lui fournissant l'UUID généré
            agent:Agent = agent_class_to_use()
        except TypeError as e:
            raise RuntimeError(f"[{self.name}] Échec d'instanciation de {agent_class_to_use}: {e}")
        
        if name:
            self._set_agent_attr(agent, 'name', name)
        if space:
            self._set_agent_attr(agent, 'space', space)
        
        print(f"[{self.name}] Agent spawné: {agent.getName()} (ID: {agent.getID()})")
        await self._trigger_callbacks('agent_created', agent.getID(), agent)
        
        if auto_initialize:
            try:
                self._call_agent_method(agent, '_onInitialize', 'onInitialize')
            except AttributeError:
                print(f"[{self.name}] Warning: L'agent n'a pas de méthode d'initialisation")
        
        with self._lock:
            self._agents[external_id] = agent
            self._agent_ids[agent] = external_id
    
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
                    print(f"[{self.name}] Warning: L'agent n'a pas de méthode onDestroy")
            
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
            print(f"[{self.name}] Agent tué: {agent_name} (ID: {agent_id})")
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
            print(f"[{self.name}] Warning: Aucun point d'entrée de réception trouvé sur l'agent")
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

class Initialize:
    """Événement d'initialisation pour les agents"""
    pass

class AgentSpawned:
    """Événement déclenché quand un agent est spawné"""
    def __init__(self, agent_id: str = None, agent_name: str = None):
        self.agent_id = agent_id
        self.agent_name = agent_name