"""
Classes for handling GUI changes from within other code.
"""

from enum import Enum, auto

class HandlerType(Enum):
    """
    Enumerate all possible UI handlers the `Player` may need to call.
    """

    on_source_changed = auto()
