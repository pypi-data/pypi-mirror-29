from __future__ import absolute_import, division, print_function, unicode_literals


"""
This module defines ros mappings and  strategies for testing (covering ros use case only).
It can be read as a specification of the current package.
"""

try:
    import genpy
except ImportError:
     import pyros_setup
     pyros_setup.configurable_import().configure().activate()
     import genpy


import six

from pyros_msgs.typecheck import (
    six_long,
    Accepter, Sanitizer, Array, Any, MinMax, CodePoint,
    TypeChecker,
    typechecker_from_rosfield_type
)


def typechecker_from_rosfield_opttype(slot_type):
    """
    Retrieves an actual type tuple based on the ros type string
    :param slot_type: the ros type string
    :return: the corresponding typeschema
    Reference :
    >>> typechecker_from_rosfield_type('bool')
    (<type 'bool'>, <type 'bool'>)
    >>> typechecker_from_rosfield_type('bool[]')
    ([<type 'bool'>], (<type 'bool'>, [<type 'bool'>]))

    >>> typechecker_from_rosfield_type('int64[]')
    ([<type 'long'>], (<type 'int'>, <type 'long'>, [(<type 'int'>, <type 'long'>)]))

    >>> typechecker_from_rosfield_type('string[]')
    ([<type 'str'>], (<type 'str'>, <type 'unicode'>, [(<type 'str'>, <type 'unicode'>)]))

    >>> typechecker_from_rosfield_type('time')  #doctest: +ELLIPSIS
    (<function <lambda> at 0x...>, {'secs': <type 'int'>, 'nsecs': <type 'int'>})
    >>> typechecker_from_rosfield_type('duration[]')  #doctest: +ELLIPSIS
    ([<function <lambda> at 0x...>], ({'secs': <type 'int'>, 'nsecs': <type 'int'>}, [{'secs': <type 'int'>, 'nsecs': <type 'int'>}]))
    """

    return typechecker_from_rosfield_type(slot_type)
    # Note : Maybe we want to recursively ignore type checking for our optional fields ? or maybe not ?
    # return typechecker_from_rosfield_type(slot_type, ignored_fields=['optional_field_initialized_', 'optional_field_names_'])
    # TODO : test it !

