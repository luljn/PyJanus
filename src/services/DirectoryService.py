# Directory Service

from agent.Agent import Agent
from .Service import Service
from typing import List, Dict, Optional
import asyncio

class DirectoryService(Service):
    
    def __init__(self):
        super().__init__()
        self._agents: Dict[str, Agent] = {}  # Stockage des agents par ID
        self._lock = asyncio.Lock()  # Pour la gestion de la concurrence
    
    def startAsync(self) -> None:
        """Démarre le service d'annuaire"""
        self._set_state("STARTING")
        # Initialisation du service
        self._set_state("RUNNING")
    
    def stopAsync(self) -> None:
        """Arrête le service d'annuaire"""
        self._set_state("STOPPING")
        # Nettoyage
        self._agents.clear()
        self._set_state("STOPPED")
    
    def awaitRunning(self) -> None:
        """Attend que le service soit en état RUNNING"""
        while self._state != "RUNNING":
            if self._state in ["STOPPED", "FAILED"]:
                raise RuntimeError("DirectoryService stopped or failed")
            import time
            time.sleep(0.1)
    
    def register_agent(self, agent: Agent) -> bool:
        """Enregistre un agent dans l'annuaire (méthode utilitaire)"""
        if agent.get_id() in self._agents:
            return False
        self._agents[agent.get_id()] = agent
        return True
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Désenregistre un agent de l'annuaire"""
        if agent_id not in self._agents:
            return False
        del self._agents[agent_id]
        return True
    
    def getAgents(self) -> List[Agent]:
        """Retourne la liste de tous les agents enregistrés"""
        return list(self._agents.values())
    
    def HasAgent(self, agent: Agent) -> bool:
        """Vérifie si un agent spécifique est présent dans l'annuaire"""
        return agent.get_id() in self._agents
    
    def getNumberOfAgents(self) -> int:
        """Retourne le nombre total d'agents enregistrés"""
        return len(self._agents)
    
    def get_agent_by_id(self, agent_id: str) -> Optional[Agent]:
        """Retourne un agent par son ID """
        return self._agents.get(agent_id)
    
    def clear(self) -> None:
        """Vide complètement l'annuaire """
        self._agents.clear()