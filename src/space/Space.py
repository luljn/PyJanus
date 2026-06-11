from uuid import UUID, uuid4
from agent.Agent import Agent
from event.Event import Event

class Space:
    def __init__(self, name: str = None):
        self.__id: UUID = uuid4()
        self.__name = name if name is not None else f'Space_{self.__id}'
        self.__participants: list[Agent] = []

    def getParticipants(self) -> list[Agent]:
        return self.__participants

    def addParticipant(self, agent: Agent) -> None:
        if agent not in self.__participants:
            self.__participants.append(agent)

    def removeParticipant(self, agent: Agent) -> None:
        """Remove agent by ID to avoid leftover references."""
        self.__participants = [a for a in self.__participants if a.getID() != agent.getID()]

    def emit(self, event: Event) -> None:
        """Send event to every participant by calling onReceiveEvent."""
        print(f"[SPACE] Broadcasting event {event.event_type} to {len(self.__participants)} participants")
        for participant in self.__participants:
            # According to the diagram: onReceiveEvent(e)
            participant.onReceiveEvent(event)

    def getID(self) -> UUID:
        return self.__id

    def getName(self) -> str:
        return self.__name