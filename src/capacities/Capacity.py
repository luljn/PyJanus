# abstract class Capacity

from abc import ABC

from agent.Agent import Agent

"""
    An interface defining what an agent can do.
    A capacity does not contain any implementation (the code will be in the Skill).
"""
class Capacity(ABC) :
    
    """
        Initializes the capability.
        :param owner: The agent that owns or uses this capability.
    """
    """ def __init__(self,owner:Agent=None) :
        self._owner = owner """

    """Returns the agent who owns this capacity."""
    def get_owner(self) :
        return self._owner
    
    """Defines the owner agent."""
    def set_owner(self, owner) :
        self._owner = owner