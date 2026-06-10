import asyncio
from .Skill import Skill
from agent.Agent import Agent
from capacities.LifeCycleCapacity import LifeCycleCapacity
from kernel.Kernel import Kernel
from services.LifeCycleService import LifeCycleService

class KillSkill(Skill, LifeCycleCapacity):
    def __init__(self):
        super().__init__()

    async def spawn(self, user: Agent, agent: Agent) -> None:
        pass

    def killme(self, user: Agent) -> None:
        agent_id = str(user.getID())
        loop = asyncio.get_event_loop()
        loop.create_task(Kernel.getInstance().getService(LifeCycleService).killAgent(agent_id))
        print(f"[SKILL] {user.getName()} requested suicide")

    def spawn_in_context(self, user: Agent, agent: Agent, context_id, *args) -> None:
        pass