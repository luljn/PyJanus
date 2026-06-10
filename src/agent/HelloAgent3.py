from asyncio import create_task
from uuid import UUID
from .Agent import Agent
from .AgentState import AgentState
from event.AgentSpawned import AgentSpawned
from event.MyEvent import MyEvent
from skills.EventSkill import EventSkill
from skills.KillSkill import KillSkill

class HelloAgent3(Agent):
    def __init__(self, id: UUID = None):
        super().__init__(id)
        self.event_skill = self.getSkill(EventSkill)
        self.kill_skill = self.getSkill(KillSkill)

    def _onInitialize(self, occurrence=None):
        super()._onInitialize()
        self.setState(AgentState.RUNNING)
        print(f"[{self.getName()}] Hello World 3")

        from kernel.Kernel import Kernel
        from services.EventService import EventService
        event_service = Kernel.getInstance().getService(EventService)
        self.listener_id = event_service.registerListener(
            "event.AgentSpawned",
            self._on_agent_spawned,
            self.getName()
        )

        create_task(self.spawnAgent("agent.HelloAgent4"))

    def _on_agent_spawned(self, event: AgentSpawned):
        # Ignore the event if it corresponds to this agent's own creation
        if event.getSource() == str(self.getID()):
            print(f"[{self.getName()}] Ignoring my own AgentSpawned event")
            return
        print(f"[{self.getName()}] Received AgentSpawned event for spawned agent -> {event}")
        my_event = MyEvent(value1=42, value2="Hello from H3")
        self.event_skill.emit(my_event, self)
        self.kill_skill.killme(self)

    def _onDestroy(self):
        pass
    def _receive(self):
        pass
    def _inSpace(self, space):
        return False
    def _leave(self):
        pass