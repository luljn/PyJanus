# abstract class Capacity

from abc import ABC

class Capacity(ABC) :
    """
        Interface définissant ce qu'un agent peut faire.
        Une capacité ne contient aucune implémentation (le code sera dans le Skill).
    """
    def __init__(self,owner=None) :
        """
            Initialise la capacité.
            :param owner: L'agent qui possède ou utilise cette capacité.
        """
        self._owner = owner

    def get_owner(self):
        """Retourne l'agent propriétaire de cette capacité."""
        return self._owner

    def set_owner(self, owner):
        """Définit l'agent propriétaire."""
        self._owner = owner