# LifeCycle Service

from .Service import Service
from typing import Dict, Optional, Any
import uuid
import asyncio
import threading

class Agent:
    """Classe représentant un agent dans le système"""
    def __init__(self, agent_id: str, name: str, space=None):
        self.id = agent_id
        self.name = name
        self.state = "CREATED"
        self.space = space
        self._running = False
    
    def onInitialize(self) -> None:
        """Méthode appelée lors de l'initialisation de l'agent"""
        self.state = "INITIALIZED"
        print(f"Agent {self.name} initialisé")
    
    def onDestroy(self) -> None:
        """Méthode appelée lors de la destruction de l'agent"""
        self.state = "DESTROYED"
        print(f"Agent {self.name} détruit")
    
    def receive(self, message: Any) -> None:
        """Reçoit un message"""
        print(f"Agent {self.name} a reçu: {message}")
    
    def isSpace(self) -> bool:
        """Vérifie si l'agent a un espace"""
        return self.space is not None
    
    def leave(self) -> None:
        """Fait quitter l'espace à l'agent"""
        if self.space:
            self.space = None
            print(f"Agent {self.name} a quitté son espace")

class Behavior:
    """Comportement d'un agent"""
    def __init__(self, owner: Agent):
        self._owner = owner
    
    def onStart(self) -> None:
        """Appelé au démarrage du comportement"""
        print(f"Comportement démarré pour {self._owner.name}")
    
    def onStop(self) -> None:
        """Appelé à l'arrêt du comportement"""
        print(f"Comportement arrêté pour {self._owner.name}")
    
    def getOwner(self) -> Agent:
        """Retourne le propriétaire du comportement"""
        return self._owner

class Initialize:
    """Classe d'initialisation des agents"""
    def __init__(self):
        self.agents = []
    
    def create_agent(self, name: str, space=None) -> Agent:
        """Crée un nouvel agent"""
        agent_id = str(uuid.uuid4())
        agent = Agent(agent_id, name, space)
        self.agents.append(agent)
        return agent

class LifeCycleService(Service):
    
    def __init__(self):
        super().__init__()
        self._agents: Dict[str, Agent] = {}
        self._behaviors: Dict[str, Behavior] = {}
        self._initializer = Initialize()
        self._lock = threading.Lock()
        self._running = False
    
    def startAsync(self) -> None:
        """Démarre le service de cycle de vie"""
        self._set_state("STARTING")
        self._running = True
        self._set_state("RUNNING")
        print("LifeCycleService démarré")
    
    def stopAsync(self) -> None:
        """Arrête le service et tous les agents"""
        self._set_state("STOPPING")
        self._running = False
        
        # Tuer tous les agents
        with self._lock:
            for agent_id in list(self._agents.keys()):
                self._kill_agent_sync(agent_id)
        
        self._set_state("STOPPED")
        print("LifeCycleService arrêté")
    
    def awaitRunning(self) -> None:
        """Attend que le service soit en état RUNNING"""
        while self._state != "RUNNING":
            if self._state in ["STOPPED", "FAILED"]:
                raise RuntimeError("LifeCycleService stopped or failed")
            import time
            time.sleep(0.1)
    
    def spawnAgent(self, name: str = None, space=None, agent_class=None, **kwargs) -> str:
        """Crée et démarre un nouvel agent"""
        if not self._running:
            raise RuntimeError("LifeCycleService n'est pas en état RUNNING")
        
        agent_id = str(uuid.uuid4())
        agent_name = name or f"Agent_{agent_id[:8]}"
        
        # Créer l'agent
        if agent_class:
            agent = agent_class(agent_id, agent_name, space, **kwargs)
        else:
            agent = Agent(agent_id, agent_name, space)
        
        # Initialiser l'agent
        agent.onInitialize()
        
        # Ajouter à la liste
        with self._lock:
            self._agents[agent_id] = agent
        
        print(f"Agent spawné: {agent_name} (ID: {agent_id})")
        return agent_id
   # Suivre l'exécution du diagramme de séquence de cr&ation du 1er Agent  
    def killAgent(self, agent_id: str) -> bool:
        """Tue un agent existant"""
        if not self._running:
            return False
        
        return self._kill_agent_sync(agent_id)
    
    def _kill_agent_sync(self, agent_id: str) -> bool:
        """Version synchrone de killAgent"""
        with self._lock:
            if agent_id not in self._agents:
                return False
            
            agent = self._agents[agent_id]
            
            # Appeler la méthode de destruction
            agent.onDestroy()
            
            # Nettoyer les comportements associés
            if agent_id in self._behaviors:
                behavior = self._behaviors[agent_id]
                behavior.onStop()
                del self._behaviors[agent_id]
            
            # Supprimer l'agent
            del self._agents[agent_id]
            
            print(f"Agent tué: {agent.name} (ID: {agent_id})")
            return True
    
    def getAgent(self, agent_id: str) -> Optional[Agent]:
        """Retourne un agent par son ID"""
        with self._lock:
            return self._agents.get(agent_id)
    
    def getAllAgents(self) -> Dict[str, Agent]:
        """Retourne tous les agents"""
        with self._lock:
            return self._agents.copy()
    
    def getNumberOfAgents(self) -> int:
        """Retourne le nombre d'agents"""
        with self._lock:
            return len(self._agents)
    
    def addBehavior(self, agent_id: str, behavior: Behavior) -> bool:
        """Ajoute un comportement à un agent"""
        with self._lock:
            if agent_id not in self._agents:
                return False
            
            self._behaviors[agent_id] = behavior
            behavior.onStart()
            return True
    
    def getBehavior(self, agent_id: str) -> Optional[Behavior]:
        """Retourne le comportement d'un agent"""
        with self._lock:
            return self._behaviors.get(agent_id)
    
    def sendMessage(self, to_agent_id: str, message: Any) -> bool:
        """Envoie un message à un agent"""
        with self._lock:
            if to_agent_id not in self._agents:
                return False
            
            agent = self._agents[to_agent_id]
            agent.receive(message)
            return True
    
    def createAndSpawnAgent(self, name: str, space=None) -> str:
        """Crée et spawn un agent via l'initializer"""
        agent = self._initializer.create_agent(name, space)
        with self._lock:
            self._agents[agent.id] = agent
        agent.onInitialize()
        return agent.id