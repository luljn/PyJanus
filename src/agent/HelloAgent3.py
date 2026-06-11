from asyncio import create_task
from uuid import UUID
import asyncio
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
        create_task(self.spawnAgent("agent.HelloAgent4"))

    def onReceiveEvent(self, event):
        if isinstance(event, AgentSpawned):
            # ignore own spawn event
            if event.getSource() != str(self.getID()):
                print(f"[{self.getName()}] Received AgentSpawned event for spawned agent -> {event}")
                # Create the MyEvent object (FIXED)
                my_event = MyEvent(value1=42, value2="Hello from H3")
                self.event_skill.emit(my_event, self)
                # Schedule suicide – the KillSkill.killme method will run in a background thread
                self.kill_skill.killme(self)

    def _onDestroy(self):
        pass
    def _receive(self):
        pass
    def _inSpace(self, space):
        return False
    def _leave(self):
        pass