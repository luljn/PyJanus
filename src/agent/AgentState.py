###

from enum import StrEnum

class AgentState(StrEnum) :
    
    INITIALIZING = 'INITIALIZING'
    RUNNING = 'RUNNING'
    DESTROYING = 'DESTROYING'