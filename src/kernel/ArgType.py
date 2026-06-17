# ArgType enum.

from enum import StrEnum

"""_summary_ : Define the type of arguments used with the command line.
"""
class ArgType(StrEnum) :
    
    FILE = 'FILE'
    MODULE = 'MODULE'