# Directory service.

from agent.Agent import Agent
from .Service import Service
from typing import List, Dict, Optional
from uuid import UUID

"""_summary_: Manages the global agents directory. 
"""
class DirectoryService(Service):
    
    # Constructor.
    def __init__(self) :
        
        super().__init__()
        self._agents: Dict[UUID, Agent] = {}
    
    # To start the service.
    async def startAsync(self) -> None :
        
        self._set_state("STARTING")
        self._set_state("RUNNING")
        print("[" + self.name + "] Service started.")
    
    # To stop the service.
    async def stopAsync(self) -> None :
        
        self._set_state("STOPPING")
        with self._lock :
            self._agents.clear()
        self._set_state("STOPPED")
        print("[" + self.name + "] Service stopped")
    
    # To register an agent to the global directory.
    def register_agent(self, agent: Agent) -> bool :
        
        with self._lock :
            
            if agent.getID() in self._agents : return False
            self._agents[agent.getID()] = agent
        
        return True
    
    # To unregister an agent from the global directory.
    def unregister_agent(self, agent: Agent) -> bool :
        
        with self._lock :
            
            if agent.getID() not in self._agents : return False
            from kernel.Kernel import Kernel
            from services.EventService import EventService
            Kernel.getInstance().getService(EventService).unregisterAgentFromSpace(agent, agent.getSpace())
            del self._agents[agent.getID()]
        
        return True
    
    # To get all the agents.
    def getAgents(self) -> List[Agent] :
        
        with self._lock : return list(self._agents.values())
    
    # To determine if an agent is present in the global directory.
    def HasAgent(self, agent: Agent) -> bool :
        
        with self._lock : return agent.getID() in self._agents
    
    # To get the number of runnin agents.
    def getNumberOfAgents(self) -> int :
        
        with self._lock : return len(self._agents)
    
    # To get an agent by its Id.
    def get_agent_by_id(self, agent_id: UUID) -> Optional[Agent] :
        
        with self._lock : return self._agents.get(agent_id)
    
    # To clear the directory.
    def clear(self) -> None :
        with self._lock : self._agents.clear()