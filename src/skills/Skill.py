# abstract class Skill

from abc import ABC, abstractmethod

from capacities.Capacity import Capacity

class Skill(ABC, Capacity) :
    
    referenceCount: int = 0
    
    @abstractmethod
    def __init__(self) :
        
        Skill.referenceCount+= 1