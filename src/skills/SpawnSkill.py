# Classe SpawnSkill
# Implémentation concrète de la capacité LifeCycleCapacity côté "création".
# Permet à un agent de spawner un autre agent via le LifeCycleService du kernel.

import asyncio
from typing import TYPE_CHECKING

from .Skill import Skill
from capacities.LifeCycleCapacity import LifeCycleCapacity

if TYPE_CHECKING :
    from agent.Agent import Agent

class SpawnSkill(Skill, LifeCycleCapacity) :

    def __init__(self, owner: "Agent" = None) :
        # On passe owner à Skill pour que ce skill sache quel agent fait le spawn.
        super().__init__(owner)

    def spawn(self, agent_class: str) -> None :
        """
        Demande au kernel de créer un nouvel agent du type donné.

        agent_class : nom de module pointé, ex: 'agent.HelloAgent4'
        C'est le même format qu'avec la commande -m de PyJanus.py.

        On délègue au LifeCycleService via le kernel (Singleton).
        spawnAgent est async, on l'appelle avec asyncio.run() depuis un contexte sync.
        """
        from kernel.Kernel import Kernel
        from services.LifeCycleService import LifeCycleService

        if self._owner is None :
            print("[SpawnSkill] Erreur : aucun agent owner defini, spawn annulé.")
            return

        asyncio.run(
            Kernel.getInstance().getService(LifeCycleService).spawnAgent(
                agent_class=agent_class
            )
        )

    def spawnWithID(self, agent_class: str, agent_id) -> None :
        """
        Variante de spawn qui permet de passer un UUID spécifique au nouvel agent.
        Utile si l'agent spawné doit avoir un identifiant prédéfini.
        """
        from kernel.Kernel import Kernel
        from services.LifeCycleService import LifeCycleService

        if self._owner is None :
            print("[SpawnSkill] Erreur : aucun agent owner defini, spawnWithID annulé.")
            return

        asyncio.run(
            Kernel.getInstance().getService(LifeCycleService).spawnAgent(
                agent_class=agent_class,
                agent_id=agent_id
            )
        )

    def killMe(self) -> None :
        # SpawnSkill ne gere pas la destruction, cette méthode est exigée par
        # LifeCycleCapacity mais n'est pas pertinente ici : utiliser KillSkill.
        pass

    def killme(self, user: "Agent") -> None :
        # Signature héritée de LifeCycleCapacity (minuscule), non pertinente ici.
        pass

    def spawn_in_context(self, user: "Agent", agent: "Agent", context_id, *args) -> None :
        # Spawn dans un contexte spécifique : non implémenté pour l'instant.
        pass