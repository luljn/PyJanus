from .Event import Event

class AgentSpawned(Event):
    def __init__(self):
        super().__init__(event_type="event.AgentSpawned")

    def __str__(self):
        return f'[Event_{self.id}] agent spawned triggered\n'