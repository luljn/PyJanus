# Skill.py

from abc import ABC, abstractmethod
from capacities.Capacity import Capacity


class Skill(Capacity, ABC):

    # attribut de classe partagé
    referenceCount = 0

    def __init__(self):
        Skill.referenceCount += 1

    @classmethod
    def get_reference_count(cls):
        return cls.referenceCount

    @abstractmethod
    def execute(self):
        """
        Méthode abstraite que chaque skill devra implémenter.
        """
        pass
