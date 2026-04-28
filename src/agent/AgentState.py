# AgentState enum

from enum import StrEnum

class AgentState(StrEnum) :
    
    NOT_RUNNING = 'NOT_RUNNING'
    INITIALIZING = 'INITIALIZING'
    RUNNING = 'RUNNING'
    DESTROYING = 'DESTROYING'