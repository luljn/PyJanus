import time
from typing import Optional

class Event:
    def __init__(self, source: Optional['Agent'] = None):
        self._source = source
        self._timestamp = time.time()

    def getSource(self) -> Optional['Agent']:
        return self._source

    def setSource(self, source: 'Agent') -> None:
        self._source = source

    def getTimestamp(self) -> float:
        return self._timestamp

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(source={self._source})"
