"""
aodho
"""

from enum import Enum, auto

class HandlerType(Enum):
    """
    Enumerate all possible handlers.
    """

    on_source_changed = auto()
