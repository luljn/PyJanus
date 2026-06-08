# abstract class Skill

from abc import ABC, abstractmethod

from capacities.Capacity import Capacity

class Skill(Capacity) :
    
    referenceCount: int = 0
    
    def __init__(self) :
        
        Skill.referenceCount+= 1