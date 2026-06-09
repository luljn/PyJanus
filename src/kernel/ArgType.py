# ArgType enum

"""_summary_ : Define the type of arguments used with the command line.
"""
from enum import StrEnum

class ArgType(StrEnum) :
    
    FILE = 'FILE'
    MODULE = 'MODULE'