# Spawn Skill

from .Skill import Skill
from capacities.LifeCycleCapacity import LifeCycleCapacity

class SpawnSkill(Skill, LifeCycleCapacity) :
    
    #
    def __init__(self) :
        
        super().__init__()