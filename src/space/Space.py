# class Space

from uuid import UUID, uuid4

from agent.Agent import Agent
from event.Event import Event

class Space :
    
    # Constructor
    def __init__(self, name: str = None) :
        
        self.__id: UUID = uuid4()
        self.__name = name if name is not None else f'Space_{self.__id}'
        self.__participants: list[Agent] = []
    
    # Get all the participants of the space.
    def getParticipants(self)-> list[Agent] :
        
        return self.__participants
    
    # Add a participant to the space.
    def addParticipant(self, agent: Agent)-> None : 
        
        self.__participants.append(agent)
    
    # To emit an event in the space.
    def emit(self, event: Event)-> None :
        
        # To ensure at least one agent will get the event.
        if self.getParticipants() :
            
            for participant in self.getParticipants() :
                
                participant._receive()
    
    # To leave the space.
    def leave(self, agent:Agent)-> None : self.getParticipants().remove(agent)
    
    # Getters
    def getID(self)-> UUID : return self.__id
    
    def getName(self)-> str : return self.__name