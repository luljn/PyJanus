from .Event import Event

class MyEvent(Event):
    def __init__(self, value1 : int = 0, value2 : str = ''):
        super().__init__()
        self.__value1 : int = value1
        self.__value2 : str = value2

    @property
    def value1(self) -> int:
        return self.__value1

    @property
    def value2(self) -> str:
        return self.__value2

    @value2.setter
    def value2(self, v : str):
        self.__value2 = v
