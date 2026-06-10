from .Skill import Skill
from agent.Agent import Agent
from capacities.EventCapacity import EventCapacity
from event.Event import Event
from kernel.Kernel import Kernel
from services.EventService import EventService
from services.DirectoryService import DirectoryService
from space.Space import Space

class EventSkill(Skill, EventCapacity):
    def __init__(self):
        super().__init__()

    def emit(self, event: Event, user: Agent, filter=None) -> None:
        event.setSource(str(user.getID()))
        event_svc = Kernel.getInstance().getService(EventService)
        # Directly queue the existing event (preserves all fields)
        event_svc.emit_event(event)
        print(f"[SKILL] {user.getName()} emitted {event}")

    def receive(self, user: Agent, event: Event) -> None:
        pass

    def wake(self, user: Agent, event: Event) -> None:
        pass

    def registerInSpace(self, agent: Agent, space: Space) -> None:
        Kernel.getInstance().getService(EventService).registerAgent(agent, space)
        Kernel.getInstance().getService(DirectoryService).register_agent(agent)