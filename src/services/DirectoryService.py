# services/DirectoryService.py - CORRECTED

from agent.Agent import Agent
from .Service import Service
from typing import List, Dict, Optional
import threading
import asyncio
from uuid import UUID

class DirectoryService(Service):
    def __init__(self):
        super().__init__()
        self._agents: Dict[UUID, Agent] = {}
        self._lock = threading.Lock()

    async def startAsync(self) -> None:
        self._set_state("STARTING")
        self._set_state("RUNNING")
        print(f"[{self.name}] Service started.")

    async def stopAsync(self) -> None:
        self._set_state("STOPPING")
        with self._lock:
            self._agents.clear()
        self._set_state("STOPPED")
        print(f"[{self.name}] Service stopped")

    async def awaitRunning(self) -> None:
        while True:
            current_state = self._state if isinstance(self._state, str) else self._state.value
            if current_state == "RUNNING":
                return
            if current_state in ["STOPPED", "FAILED"]:
                raise RuntimeError("DirectoryService stopped or failed")
            await asyncio.sleep(0.1)

    def register_agent(self, agent: Agent) -> bool:
        with self._lock:
            if agent.getID() in self._agents:
                return False
            self._agents[agent.getID()] = agent
            print(f"[DIRECTORY] Agent {agent.getName()} (ID: {agent.getID()}) registered")
            return True

    def unregister_agent(self, agent_id: str) -> bool:
        """agent_id is a string representation of UUID."""
        try:
            uid = UUID(agent_id)
        except ValueError:
            return False
        with self._lock:
            if uid not in self._agents:
                return False
            agent = self._agents.pop(uid)
            print(f"[DIRECTORY] Agent {agent.getName()} (ID: {agent.getID()}) unregistered")
            return True

    def getAgents(self) -> List[Agent]:
        with self._lock:
            return list(self._agents.values())

    def HasAgent(self, agent: Agent) -> bool:
        with self._lock:
            return agent.getID() in self._agents

    def getNumberOfAgents(self) -> int:
        with self._lock:
            return len(self._agents)

    def get_agent_by_id(self, agent_id: str) -> Optional[Agent]:
        try:
            uid = UUID(agent_id)
        except ValueError:
            return None
        with self._lock:
            return self._agents.get(uid)

    def clear(self) -> None:
        with self._lock:
            self._agents.clear()

    def getDictAgents(self) -> Dict[UUID, Agent]:
        return self._agents