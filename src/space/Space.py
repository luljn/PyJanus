# class Space

from agent.Agent import Agent

class Space :
    
    #
    def __init__(self) :
        
        self.__participants: list[Agent] = []
    
    #
    def getParticipants(self)-> list[Agent] :
        
        return self.participants
    
    #
    def addParticipant(self, agent: Agent)-> None : 
        
        self.__participants.append(agent)