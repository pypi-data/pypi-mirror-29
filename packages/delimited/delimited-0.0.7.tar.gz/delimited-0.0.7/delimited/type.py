"""
delimited.type
~~~~~~~~~~~~~~~~~

This module defines...
"""

from delimited.container import NestedContainer
from delimited.mapping import NestedMapping
from delimited.sequence import NestedSequence
from delimited.sequence import ListIndex


class NestedType(object):

    def __new__(cls, name, path):

        mapping = type(
            f"{name.title()}Dict",
            (NestedMapping, NestedContainer),
            {
                "container": dict,
                "path": path
            }
        )

        sequence = type(
            f"{name.title()}List",
            (NestedSequence, NestedContainer),
            {
                "container": list,
                "path": path,
                "sequenceindex": ListIndex,
            }
        )
        
        mapping.mapping = sequence.mapping = mapping
        mapping.sequence = sequence.sequence = sequence
        
        return mapping, sequence
