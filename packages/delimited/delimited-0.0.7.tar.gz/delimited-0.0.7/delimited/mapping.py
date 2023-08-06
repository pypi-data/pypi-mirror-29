"""
delimited.mapping
~~~~~~~~~~~~~~~~~

This module defines NestedMapping objects. A NestedMapping object
implements an interface through which nested data can be accessed and
modified using Path objects.
"""


class NestedMapping(object):
    """ The abstract base class for NestedMapping objects. When subclassing
    NestedMapping the path and container attributes must be overridden with a
    Path object and container type respectively. The path object chosen defines
    the collapsed path format used by the NestedMapping class.
    """

    def __iter__(self):
        """ Yield key, value tuples for instance data.
        """

        for key, value in self.data.items():
            yield key, value

    def items(self):
        """ Yield key, value tuples for instance data.
        """

        for key, value in self.data.items():
            yield (key, value)

    def keys(self):
        """ Yield keys for instance data.
        """

        for key in self.data.keys():
            yield key

    def values(self):
        """ Yield values for instance data.
        """

        for value in self.data.values():
            yield value

    def update(self, data, path=None):
        """ Update instance data at path with data.
        """

        if isinstance(data, self.__class__):
            data = data.unwrap()

        self.ref(path).update(data)
