# LifeCycle service.

from importlib import import_module
from typing import Optional

from .Service import Service
from agent.Agent import Agent
from agent.AgentState import AgentState
from behavior.Behavior import Behavior
from event.Event import Event
from space.Space import Space

"""_summary_: Manages agent Life cycle.
"""
class LifeCycleService(Service):
    
    # Contructor.
    def __init__(self) :
        """Initialize the LifeCycleService."""
        super().__init__()
        self._running = False
    
    # To start the service.
    async def startAsync(self) -> None :
        
        self._set_state("STARTING")
        self._running = True
        self._thread.start()
        self._set_state("RUNNING")
        print("[" + self.name + "] Service started.")
    
    # To stop the service.
    async def stopAsync(self) -> None :
        
        self._set_state("STOPPING")
        self._running = False
        print("[" + self.name + "] Service stopped")
        
        self._set_state("STOPPED")
    
    # To call a method of an agent.
    def _call_agent_method(self, agent, private_method_name: str, fallback_name: str, *args, **kwargs):
        """Dynamically calls a method of the agent (protected or private)."""
        class_name = agent.__class__.__name__
        
        # 1. Try with the protected name (ex: '_onInitialize')
        if hasattr(agent, private_method_name):
            return getattr(agent, private_method_name)(*args, **kwargs)
            
        # 2. Fallback on the alternative private method (ex: '__onInitialize')
        if hasattr(agent, fallback_name):
            return getattr(agent, fallback_name)(*args, **kwargs)
            
        # 3. If no one exists
        raise AttributeError("[" + self.name + "] L'agent " + class_name + " n'a ni la méthode " + private_method_name + ", ni " + fallback_name)
    
    # Spawn an agent.
    async def spawnAgent(self, name: Optional[str] = None, space:Space=None, agent_class:str=None, 
                         **kwargs) -> None :
        
        if not self._running : raise RuntimeError("[" + {self.name} + "] Service is not in RUNNING state")
        
        agent_class_to_use = getattr(import_module(agent_class), agent_class.split('.')[-1])
        
        if not agent_class_to_use : raise RuntimeError("[" + {self.name} + "] No Agent class given.")
        
        try :
            
            # Agent creation and initialization.
            agent:Agent = agent_class_to_use() 
            print("[INFO] Agent " + agent.getName() + " created")
            Initialize.initialize(agent, self)
        
        except TypeError as e :
            
            raise RuntimeError("[" + self.name + "] Instantiation failed " + str(agent_class_to_use) + " : " + str(e))
        
        if name : agent.setName(name)
        
        from kernel.Kernel import Kernel
            
        if space : agent.register(space)
        
        elif (not space) : agent.register(Kernel.getInstance().getDefaultSpace())
        
        from services.EventService import EventService
        from services.DirectoryService import DirectoryService
        Kernel.getInstance().getService(EventService).emit(self.emitAgentSpawned(agent))
        print("\n[" + self.name + "] Agent spawned-> Name: " + agent.getName() + " - ID: " + str(agent.getID()) + " - Type: " + agent.__class__.__name__ + "\n")
        print("Number of running agent : " + str(Kernel.getInstance().getService(DirectoryService).getNumberOfAgents()) + "\n")
    
    # To kill an agent.
    async def killAgent(self, agent:Agent) :
        
        from kernel.Kernel import Kernel
        from services.DirectoryService import DirectoryService
        Kernel.getInstance().getService(DirectoryService).unregister_agent(agent)
        self._call_agent_method(agent, '_onDestroy', '__onDestroy')
        from services.EventService import EventService
        Kernel.getInstance().getService(EventService).emit(self.emitAgentDestroyed(agent))
        del agent
        print("Number of running agent : " + str(Kernel.getInstance().getService(DirectoryService).getNumberOfAgents()) + "\n")
    
    # To emit AgentSpawned event.
    def emitAgentSpawned(self, agent:Agent)->Event : 
        
        from event.AgentSpawned import AgentSpawned
        event:AgentSpawned = AgentSpawned(source=self, data="Agent " + agent.getName() + " was spawned")
        return event
    
    # To emit AgentDestroyed event.
    def emitAgentDestroyed(self, agent: Agent)->Event :
        
        from event.AgentDestroyed import AgentDestroyed
        event:AgentDestroyed = AgentDestroyed(source=self, data="Agent " + agent.getName() + " was detroyed")
        return event

"""_summary_ : class Initialize"""
class Initialize :
    
    """Initialization of agents"""
    @staticmethod
    def initialize(agent: Agent, service:LifeCycleService)-> None : 
        print("Initialization of agent " + agent.getName())
        agent.setState(AgentState.INITIALIZING)
        service._call_agent_method(agent, '_onInitialize', '__onInitialize')
        return None