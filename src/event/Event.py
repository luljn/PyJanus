# class Event

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4



class Event :
    
    # Constructor.
    def __init__(self, id:UUID = None, source:Any = None, data:Any = None, timestamp:datetime = datetime.now()) :
        
        self.id = uuid4() if id is None else id
        self.source = source
        self.data = data
        self.timestamp = timestamp
    
    # To get the source of the event.
    def getSource(self)-> Any :
        
        return self.source
    
    # To set the source of the event.
    def setSource(self, source_:Any)-> None :
        
        self.source = source_
    
    # toString equivalent in Python.
    def __str__(self)-> None :
        
        return f'Event_{self.id} trigerred\ndata : {self.data}\n'
    
    # To get the ID.
    def getID(self)->UUID : return self.id