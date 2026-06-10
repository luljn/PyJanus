# event/Event.py

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

class Event:
    def __init__(self, id: UUID = None, source: str = None, data: Any = None,
                 timestamp: datetime = datetime.now(), event_type: str = None):
        self.id = uuid4() if id is None else id
        self.source = source
        self.data = data
        self.timestamp = timestamp
        self.event_type = event_type if event_type else self.__class__.__name__

    def getSource(self) -> str:
        return self.source

    def setSource(self, source_: str) -> None:
        self.source = source_

    def __str__(self) -> str:
        return f'Event with id {self.id} triggered\n'