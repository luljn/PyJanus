from uuid import UUID
from .Agent import Agent
from .AgentState import AgentState
from event.MyEvent import MyEvent
from skills.KillSkill import KillSkill

class HelloAgent4(Agent):
    def __init__(self, id: UUID = None):
        super().__init__(id)
        self.kill_skill = self.getSkill(KillSkill)

    def _onInitialize(self, occurrence=None):
        super()._onInitialize()
        self.setState(AgentState.RUNNING)
        print(f"[{self.getName()}] Hello World 4")

    def onReceiveEvent(self, event):
        if isinstance(event, MyEvent):
            print(f"[{self.getName()}] Received MyEvent: value1={event.value1}, value2={event.value2}")
            self.kill_skill.killme(self)

    def _onDestroy(self):
        pass
    def _receive(self):
        pass
    def _inSpace(self, space):
        return False
    def _leave(self):
        pass