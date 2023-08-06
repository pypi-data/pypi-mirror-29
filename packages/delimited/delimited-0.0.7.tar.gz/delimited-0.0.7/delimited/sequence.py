"""
delimited.sequence
~~~~~~~~~~~~~~~~~~

This module defines...
"""

# index


class SequenceIndex(object):
    sequence = None
    
    def __init__(self, index):
        if not isinstance(index, int):
            raise TypeError(index)
        self.index = index
        
    def __str__(self):
        return str(self.index)
        
    def __repr__(self):
        return f'{self.__class__.__name__}({self.index})'
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.index == other.index
        if isinstance(other, int):
            return self.index == other
        return False
        
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __hash__(self):
        return hash(str(self.index))


class ListIndex(SequenceIndex):
    sequence = list


# value


class SequenceValue(object):
    pass


# sequence


class NestedSequence(object):
    sequenceindex = None
        
    def __add__(self, other):
        
        if isinstance(other, self.__class__):
            data = other.data
        elif isinstance(other, self.container):
            data = other
        
        return self.__class__(self.data + data)
        
    def __iadd__(self, other):
        
        if isinstance(other, self.__class__):
            data = other.data
        elif isinstance(other, self.container):
            data = other
            
        self.data += other
        
        return self
        
    def __iter__(self):
        for v in self.data:
            yield v
        
    def __reversed__(self):
        for v in self.data[::-1]:
            yield v
        
    def append(self, value):
        return self.data.append(value)
        
    def extend(self, other):
        if isinstance(other, self.__class__):
            data = other.data
        elif isinstance(other, self.container):
            data = other
        
        return self.data.extend(data)
        
    def insert(self, i, value):
        return self.data.insert(i, value)
        
    def remove(self, value):
        return self.data.remove(value)
        
    def pop(self, *args):
        return self.data.pop(*args)
        
    def clear(self):
        return self()
        
    def index(self, value):
        return self.data.index(value)
        
    def count(self, value):
        return self.data.count(value)
        
    def reverse(self):
        self.data = self.data[::-1]
