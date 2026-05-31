# class Space

from uuid import UUID, uuid4

class Space :
    
    # Constructor
    def __init__(self, name: str = None) :
        
        self.__id: UUID = uuid4()
        self.__name = name if name is not None else f'Default_Space_{self.__id}'
        self.__participants: list[UUID] = []
    
    # Get all the participants of the space
    def getParticipants(self)-> list[UUID] :
        
        return self.__participants
    
    # Add a participant to the space.
    def addParticipant(self, agentId: UUID)-> None : 
        
        self.__participants.append(agentId)
    
    # To emit an event in the space.
    def emit() :
        pass
    
    # Getters
    def getID(self)-> UUID :
        return self.__id
    
    def getName(self)-> UUID :
        return self.__name