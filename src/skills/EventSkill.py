# Classe EventSkill
# Implémentation concrète de la capacité EventCapacity.
# Permet à un agent d'émettre des événements et de s'enregistrer dans un Space.

from typing import TYPE_CHECKING

from .Skill import Skill
from capacities.EventCapacity import EventCapacity
from kernel.Kernel import Kernel
from services.EventService import EventService
from services.DirectoryService import DirectoryService
from space.Space import Space

if TYPE_CHECKING :
    from agent.Agent import Agent
    from event.Event import Event

class EventSkill(Skill, EventCapacity) :

    def __init__(self, owner: "Agent" = None) :
        # On passe owner à Skill pour identifier l'agent émetteur lors du emit.
        super().__init__(owner)

    def emit(self, event_type: str = "event.Event") -> None :
        """
        Émet un événement dans le bus d'événements via l'EventService.
        event_type : nom du module de l'événement, ex: 'event.MyEvent'.
        La source de l'événement est l'ID de l'agent owner (sous forme de str).
        """
        if self._owner is None :
            print("[EventSkill] Erreur : aucun agent owner defini, emit annulé.")
            return

        Kernel.getInstance().getService(EventService).emit(
            event_type=event_type,
            # On identifie la source de l'événement par l'ID de l'agent émetteur.
            source=str(self._owner.getID())
        )

    def receive(self, user: "Agent", event: "Event") -> None :
        # La réception d'événement est gérée par les méthodes __guard_X__ de l'agent,
        # pas directement par ce skill. Méthode exigée par EventCapacity.
        pass

    def wake(self, user: "Agent", event: "Event") -> None :
        # Réveil des comportements en attente d'un événement : non implémenté.
        pass

    def registerInSpace(self, agent: "Agent", space: Space) -> None :
        """
        Enregistre l'agent dans un Space ET dans le DirectoryService.
        - EventService.registerAgent : ajoute l'agent à la liste des participants du space.
        - DirectoryService.register_agent : ajoute l'agent au registre global des agents actifs.
        Ces deux enregistrements sont toujours faits ensemble.
        """
        Kernel.getInstance().getService(EventService).registerAgent(agent, space)
        Kernel.getInstance().getService(DirectoryService).register_agent(agent)