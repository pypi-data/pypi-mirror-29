from delimited.type import NestedType
from delimited.path import TuplePath
from delimited.path import DelimitedStrPath


__version__ = "0.0.7"
__title__ = "delimited"
__summary__ = "Defines types that allow for accessing and modifying nested data"
__url__ = "https://github.com/chrisantonellis/delimited"
__author__ = "Christopher Antonellis"
__email__ = "christopher.antonellis@gmail.com"
__license__ = "MIT License"


NestedDict, NestedList = NestedType("nested", TuplePath)
DelimitedDict, DelimitedList = NestedType("delimited", DelimitedStrPath)