from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Evite les imports circulaires
if TYPE_CHECKING:
    from agent.Agent import Agent


class Behavior(ABC):

    def __init__(self, owner: "Agent" = None):

        # Agent propriétaire
        self.owner = owner

        # Etat du behavior
        self.running = False

    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_stop(self):
        pass

    def start(self):

        if not self.running:
            self.running = True
            self.on_start()

    def stop(self):

        if self.running:
            self.running = False
            self.on_stop()

    def get_owner(self) -> "Agent":
        return self.owner

    def set_owner(self, owner: "Agent"):
        self.owner = owner

    def as_event_listener(self):
        return self

    def is_running(self):
        return self.running