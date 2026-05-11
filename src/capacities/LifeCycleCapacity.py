
from abc import abstractmethod

from Capacity import Capacity


class LifeCycleCapacity(Capacity):
    """
        Capacité définissant les actions liées au cycle de vie de l'agent.
    """
    def __init__(self, owner=None):
        super().__init__(owner)

    @abstractmethod
    def spawn(self, agent_type: type,*args) -> None:
        """
                Crée une nouvelle instance d'agent d'un type donné.
        """
        pass

    @abstractmethod
    def killme(self) -> None:
        """
                Demande l'arrêt et la destruction de l'agent actuel.
        """
        pass

    @abstractmethod
    def spawn_in_context(self, agent_type: type, context_id, *args) -> None:
        """Crée un agent dans un contexte spécifique."""
        pass