###

from agent.Agent import Agent
from .Service import Service

class DirectoryService(Service) : 
    
    #
    def __init__(self) :
        
        super().__init__()
    
    #
    def getAgents(self)-> list[Agent] :
        
        pass
    
    #
    def HasAgent(self, a: Agent)-> bool :
        
        return False
    
    #
    def getNumberOfAgents(self)-> int :
        
        return self.getAgents().__len__