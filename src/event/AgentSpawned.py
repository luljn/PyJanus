# class AgentSpawned

from datetime import datetime
from typing import Any
from uuid import UUID

from .Event import Event



"""Event triggered when an agent is spawned"""
class AgentSpawned(Event) :
    
    def __init__(self, id:UUID = None, source:Any = None, data:Any = None, timestamp:datetime = datetime.now()) :
        
        super().__init__(id, source, data, timestamp)
    
    def __str__(self)-> None :
        
        return f'[Event_{self.id}] agent spawned trigerred\ndata : {self.data}\n'