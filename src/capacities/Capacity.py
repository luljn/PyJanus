# abstract class Capacity

from abc import ABC

"""
    An interface defining what an agent can do.
    A capacity does not contain any implementation (the code will be in the Skill).
"""
class Capacity(ABC) :
    
    """Returns the agent who owns this capacity."""
    def get_owner(self) :
        return self._owner
    
    """Defines the owner agent."""
    def set_owner(self, owner) :
        self._owner = owner