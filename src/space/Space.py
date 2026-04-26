###

from agent.Agent import Agent

class Space :
    
    #
    def __init__(self) :
        
        self.participants: list[Agent] = []
    
    #
    def getParticipants(self)-> list[Agent] :
        
        return self.participants