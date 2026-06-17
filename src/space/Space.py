# class Space.

from uuid import UUID, uuid4

from agent.Agent import Agent
from event.Event import Event

"""_summary_ : Place where agents are registered.
"""
class Space :
    
    # Constructor.
    def __init__(self, name: str = None) :
        
        self.__id: UUID = uuid4()
        self.__name = name if name is not None else "Space_" + str(self.__id)
        self.__participants: list[Agent] = []
    
    # Get all the participants of the space.
    def getParticipants(self)-> list[Agent] :
        
        return self.__participants
    
    # Add a participant to the space.
    def addParticipant(self, agent: Agent)-> None : 
        
        self.__participants.append(agent)
    
    # To send an event in the space.
    def send(self, event: Event)-> None :
        
        print("Event " + event.__class__.__name__+ "_" + str(event.getID()) + " sent to space " + self.getName() + "\n")
        
        # To ensure at least one agent will get the event.
        if self.getParticipants() :
            
            for participant in self.getParticipants() :
                
                if not participant.getName() in event.data :
                    participant._receive(event)
    
    # To leave the space.
    def unregister(self, agent:Agent)-> None : self.getParticipants().remove(agent)
    
    # Getters.
    def getID(self)-> UUID : return self.__id
    
    def getName(self)-> str : return self.__name