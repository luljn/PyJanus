# AgentState enum.

from enum import StrEnum

"""_summary_ : Define the state of an agent.
"""
class AgentState(StrEnum) :
    
    NOT_RUNNING = 'NOT_RUNNING'
    INITIALIZING = 'INITIALIZING'
    RUNNING = 'RUNNING'
    DESTROYING = 'DESTROYING'