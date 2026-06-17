# class Event.

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

"""_summary_ : Event base class.
"""
class Event :
    
    # Constructor.
    def __init__(self, id:UUID = None, source:Any = None, data:Any = None, timestamp:datetime = datetime.now()) :
        
        self.id = uuid4() if id is None else id
        self.source = source
        self.data = data
        self.timestamp = timestamp
    
    # To get the ID.
    def getID(self)->UUID : return self.id
    
    # To get the source of the event.
    def getSource(self)-> Any :
        
        return self.source
    
    # To get the data of the event.
    def getData(self)-> Any :
        
        return self.data
    
    # To set the source of the event.
    def setSource(self, source_:Any)-> None :
        
        self.source = source_
    
    # To set the data of the event.
    def setData(self, data_:Any)-> None :
        
        self.data = data_
    
    # __str__ method overriding (toString equivalent in Python).
    def __str__(self)-> None :
        
        return "Event_" + str(self.getID()) + " trigerred\ndata : " + str(self.getData()) + "\n"