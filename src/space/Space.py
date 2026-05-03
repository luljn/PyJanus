# class Space

from uuid import UUID

class Space :
    
    #
    def __init__(self) :
        
        self.__participants: list[UUID] = []
    
    #
    def getParticipants(self)-> list[UUID] :
        
        return self.__participants
    
    #
    def addParticipant(self, agentId: UUID)-> None : 
        
        self.__participants.append(agentId)