# abstract class Skill.

from capacities.Capacity import Capacity

"""_summary_ : Skill base class.
"""
class Skill(Capacity) :
    
    referenceCount: int = 0
    
    def __init__(self) :
        
        Skill.referenceCount+= 1