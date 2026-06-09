# class AgentSpawned

from .Event import Event



"""Event triggered when an agent is spawned"""
class AgentSpawned(Event) :
    
    def __init__(self) :
        
        super().__init__()
    
    def __str__(self)-> None :
        
        return f'[Event_{self.id}] agent spawned trigerred\n'