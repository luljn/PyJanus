# class AgentDestroyed.

from datetime import datetime
from typing import Any
from uuid import UUID

from .Event import Event

"""_summary_ : Event triggered when an agent is destroyed.
"""
class AgentDestroyed(Event) :
    
    # Constructor.
    def __init__(self, id:UUID = None, source:Any = None, data:Any = None, timestamp:datetime = datetime.now()) :
        
        super().__init__(id, source, data, timestamp)
    
    # __str__ method overriding.
    def __str__(self)-> None :
        
        return "[Event_" + str(self.id) + " agent destroyed trigerred\ndata : " + str(self.data) + "\n"