from __future__ import absolute_import, division, print_function, unicode_literals

# PY2 Py3 ref : http://python-future.org/compatible_idioms.html

"""
TypeSchemas add extra type checking on basic python types.
Especially they add structure checks (to match ROS message types), instead of the usual python duck-typing.

This is required to detect error in a ROS message structure when it is built, instead of when it is received.
It prevents ROS message type error propagation from one node to another.

This module implement the core functionality for typeschemas, as independently as possible from implementation.
The goal here is to have a semantic representation (using python data types for simplicity) of ROS message/field types.

In a ROS message, a field can have a value of one of the basic types :
- bool,
- int, (careful with long and python2)
- float,
- string, (careful with unicode and python2)
- time,
- duration

or of a composed type T :
- array/list
- another message type ( = dict of fields' types )

For a value V, being of any one of the types T or T' is represented by a namedtuple (sanitize=f, accept=g),
where g is defined as "lambda v : isinstance(v, (T, T'))"
Even if any types could be 'accepted', the function in the first element
will be called to convert from other accepted types into the sanitized type ST.
So f is defined as "lambda v : ST(v)"

For a value V, being an array of one type T is represented by a schema list [T]
By extension, for a value V, being an array of any one of the types T or T'
is represented by a schema list with a tuple [(T, T')]
Note [(T,)] <=> [T]

A message type is represented by a schema dict {}.
The keys denote the message fields names, and the values are the types, following the previous rules.
"""

import sys
import six
# to get long for py2 and int for py3
six_long = six.integer_types[-1]

import copy

def maybe_list(l):
    """Return list of one element if ``l`` is a scalar."""
    return l if l is None or isinstance(l, list) else [l]


def maybe_tuple(t):
    """Return tuple of one element if ``t`` is a scalar."""
    return t if t is None or isinstance(t, tuple) else (t,)


def maybe_set(t):
    """Return tuple of one element if ``t`` is a scalar."""
    return t if t is None or isinstance(t, set) else {t}


#
# SANITIZERS for field types
# Used to construct a new default value or to modify a value passed as argument
#


# Using classes and object hierarchy to represent sanitizer and accepter functions
# since python prefers that to functions or types
class Sanitizer(object):
    def __init__(self, t):
        self.t = t

    def __call__(self, *args, **kwargs):
        if kwargs and hasattr(self.t, '__dict__'): # if self.t is an (new-style) object, it specifies how to sanitize, ie it is a filter
            # TODO : is this actually useful / used ??
            return self.t(**{
                subk: subt.sanitizer(kwargs.get(subk))
                for subk, subt in vars(self.t).items()
            })
            #TODO : is it the same with slots ?
        elif args:  # basic type (or mapping type but we pass a full value)
            # we sanitize by running the type initializer with the value
            if self.t == six.binary_type:
                # we need to encode
                initializer = args[0]
                # Ref : https://www.python.org/dev/peps/pep-0358/
                if isinstance(initializer, six.text_type) and sys.version_info > (3, 0):
                    encoding = args[1] if len(args) > 1 else sys.getdefaultencoding()
                    return self.t(initializer, encoding)
                elif initializer is not None:
                    return self.t(initializer)
                else:
                    return self.t()
            elif self.t == six.text_type:
                # we need to decode
                obj = args[0]
                if isinstance(args[0], six.binary_type):
                    obj.decode(sys.getdefaultencoding())
                return self.t(obj)
            else:
                return self.t(
                    *(a for a in args if a is not None))  # careful we do not want to pass None to a basic type
        else:
            TypeCheckerException("Calling {self} with {args} and {kwargs}. not supported".format(**locals()))

    def __repr__(self):
        return "Sanitizer to {self.t}".format(**locals())

#
# ACCEPTERS for field types
# Used to certify the type match (duck typing for composed types)
#

# TODO : optional value -> support None... ?


class Accepter(object):
    def __init__(self, t):
        self.t = t

    def __call__(self, v=None):
        # TODO : we probably want to get args and kwargs here to match "any" kind of function call (like for sanitizer)
        # It might be helpful when we have unstrictly specified nested types instance...
        if self.t is None:  # if our accepted type is none we only accept none
            return v is None
        elif isinstance(self.t, dict):
            return all(hasattr(v, s) and self.t.get(s).accepter(getattr(v, s)) for s, st in self.t.items())
        else:  # basic type
            return isinstance(v, self.t)

    def __repr__(self):
        return "Accepter from {self.t}".format(**locals())


#
# Operators on Sanitizer or Accepter
#

class MinMax(object):
    def __init__(self, at, min_val, max_val):
        assert isinstance(at, (Accepter, Any))  # Note MinMax makes sense only for Accepter or Any
        self.at = at
        self.min = min_val
        self.max = max_val

    def __call__(self, v):
        return self.at(v) and self.min <= v <= self.max

    def __repr__(self):
        return "MinMax [{self.min}..{self.max}] of {self.at}".format(**locals())


class CodePoint(object):
    def __init__(self, at, min_cp, max_cp):
        assert isinstance(at, (Accepter, Any))  # Note CodePoint makes sense only for Accepter or Any
        self.at = at
        self.min = min_cp
        self.max = max_cp

    def __call__(self, v):
        return self.at(v) and all(self.min <= ord(c) <= self.max for c in v)

    def __repr__(self):
        return "CodePoint [{self.min}..{self.max}] of {self.at}".format(**locals())


class Any(object):  # Any has the same meaning as a set of accepters...
    def __init__(self, *at):
        assert all(isinstance(aet, (Accepter, Array, MinMax, CodePoint, Any)) for aet in at)  # Note Any makes sense only for Accepter
        self.at = {st for st in at}

    def __call__(self, v):
        return any(st(v) for st in self.at)

    def __repr__(self):
        return "Any of {self.at}".format(**locals())  # set-like repr since the meaning ov any is similar to set


class Array(object):
    def __init__(self, t):
        """
        Array can be used with both sanitizer or accepter.
        It has different meaning for each
        :param t: the sanitizer or accepter to use for each element
        """
        assert isinstance(t, (Sanitizer, Accepter, Any, MinMax, Array))
        self.t = t

    def __call__(self, v=None):
        if not isinstance(v, list) and v is not None:  # we need to force the value to be a list
            return False
        if isinstance(self.t, (Sanitizer, )):
            # Array mean generate an array
            return [self.t(e) for e in v] if v is not None else []
        elif isinstance(self.t, (Accepter, Any, MinMax, CodePoint)):
            # Array mean check all elements
            return all(self.t(e) for e in v) if v is not None else self.t(None)
        else:  # should never happen
            raise TypeCheckerException("function for Array is neither a Sanitizer or an Accepter, Any, MinMax, CodePoint")

    def __repr__(self):
        return "Array of {self.t}".format(**locals())


class TypeCheckerException(Exception):
    """An Exception supporting unicode message"""
    def __init__(self, message):

        if isinstance(message, six.text_type):
            super(TypeCheckerException, self).__init__(message.encode('utf-8', 'replace'))
            self.message = message

        elif isinstance(message, six.binary_type):
            super(TypeCheckerException, self).__init__(message)
            self.message = message.decode('utf-8', 'replace')

        else:      # This shouldn't happen...
            raise TypeError("message in an exception has to be a string (optionally unicode)")

    def __str__(self):  # when we need a binary string
        return self.message.encode('ascii', 'replace')

    def __unicode__(self):  # when we need a text string
        return self.message

    def __repr__(self):
        return "TypeCheckerException(" + self.message + ")"


class TypeChecker(object):
    def __init__(self, sanitizer, accepter):
        """
        :param sanitizer: a function to be used as sanitizer
        :param accepter: a function to be used as accepter
        """

        self.sanitizer = sanitizer
        self.accepter = accepter

    def __call__(self, value=None):
        """
        TypeCheck (with accepter) and sanitize (with sanitizer) the value.
        Returns an exception if the value cannot be accepted.
        Sanitizer may also return an exception if conversion is not possible.
        :param value: the value to typecheck
        :return: sanitized value

        Examples with bool and bool array :
        >>> bool_tc = TypeChecker(Sanitizer(bool), Accepter(bool))
        >>> bool_tc(True)
        True
        >>> bool_tc([True])
        Traceback (most recent call last):
        ...
        TypeCheckerException: '[True]:<type 'list'>' is not accepted by Accepter from <type 'bool'>
        >>> bool_tc([True, False])
        Traceback (most recent call last):
        ...
        TypeCheckerException: '[True, False]:<type 'list'>' is not accepted by Accepter from <type 'bool'>
        >>> boolarray_tc = TypeChecker(Array(Sanitizer(bool)), Array(Accepter(bool)))
        >>> boolarray_tc(True)
        Traceback (most recent call last):
        ...
        TypeCheckerException: 'True:<type 'bool'>' is not accepted by Array of Accepter from <type 'bool'>
        >>> boolarray_tc([False])
        [False]
        >>> boolarray_tc([False, True])
        [False, True]

        Examples with int :
        >>> int_tc = TypeChecker(Sanitizer(int), Accepter(int))
        >>> int_tc(42)
        42
        >>> intarray_tc = TypeChecker(Array(Sanitizer(int)), Array(Accepter(int)))
        >>> intarray_tc([42])
        [42]
        >>> intoptarray_array_tc = TypeChecker(Array(Sanitizer(int)), Array(Any(Accepter(int), Array(Accepter(int)))))
        >>> intoptarray_array_tc([[42], 23])
        Traceback (most recent call last):
        ...
        TypeCheckerException: '[[42], 23]:<type 'list'>' cannot be sanitized by Array of Sanitizer to <type 'int'>
                      Reason: int() argument must be a string or a number, not 'list'
        >>> longarray_tc = TypeChecker(Array(Sanitizer(six_long)), Array(Accepter(six_long)))
        >>> longarray_tc(six_long(42))
        Traceback (most recent call last):
        ...
        TypeCheckerException: '42:<type 'long'>' is not accepted by Array of Accepter from <type 'long'>
        >>> intarray_tc = TypeChecker(Array(Sanitizer(int)), Array(Accepter(int)))
        >>> intarray_tc([six_long(42)])
        Traceback (most recent call last):
        ...
        TypeCheckerException: '[42L]:<type 'list'>' is not accepted by Array of Accepter from <type 'int'>
        >>> intlongarray = TypeChecker(Array(Sanitizer(six_long)), Array(Any(Accepter(int), Accepter(six_long))))
        >>> intlongarray([42, six_long(42)])
        [42L, 42L]

        We can also check min and max bounds
        >>> intlongarray = TypeChecker(Array(Sanitizer(int)), Array(Any(Accepter(int), MinMax(Accepter(six_long),0,255))))
        >>> intlongarray([42, six_long(42)])
        [42, 42]
        >>> intlongarray = TypeChecker(Array(Sanitizer(int)), Array(Any(Accepter(int), MinMax(Accepter(six_long),0,255))))
        >>> intlongarray([42, six_long(234234234234234234234)])
        Traceback (most recent call last):
        ...
        TypeCheckerException: '[42, 234234234234234234234L]:<type 'list'>' is not accepted by Array of Any of set([Accepter from <type 'int'>, MinMax [0..255] of Accepter from <type 'long'>])

        Examples with complex types
        >>> class Custom(object):
        ...     def __init__(self, d1=0, d2=''):
        ...         self.d1 = d1; self.d2 = d2
        ...     def __repr__(self):
        ...         return "d1:{d1} d2:{d2}".format(d1=self.d1, d2=self.d2)
        >>> custom_msg = Custom(42, d2='bla')

        with a simple sanitizing function
        >>> customd1_sanitizer = lambda x=None: Custom(d1=x.d1) if x else Custom()
        >>> customd1_tc = TypeChecker(Sanitizer(customd1_sanitizer), Accepter({
        ...     'd1': TypeChecker(Sanitizer(int), Accepter(int))
        ... }))
        >>> customd1_tc(custom_msg)
        d1:42 d2:

        we can filter some members on the sanitizing function
        >>> customd1d2_sanitizer = lambda x=None: Custom(d1=x.d1, d2=x.d2) if x else Custom()
        >>> customd1d2_tc = TypeChecker(Sanitizer(customd1d2_sanitizer), Accepter({
        ...     'd1': TypeChecker(Sanitizer(int),Accepter(int)),
        ...     'd2': TypeChecker(Sanitizer(str), Any(Accepter(str), Accepter(unicode)))
        ... }))
        >>> customd1d2_tc(custom_msg)
        d1:42 d2:bla

        >>> customd1d2_tc = TypeChecker(Sanitizer(customd1d2_sanitizer), Accepter({
        ...     'd1': TypeChecker(Sanitizer(int),Accepter(int)),
        ...     'bad_field': TypeChecker(Sanitizer(int),Accepter(int))
        ... }))
        >>> customd1d2_tc(custom_msg)
        Traceback (most recent call last):
        ...
        TypeCheckerException: 'd1:42 d2:bla:<class 'typechecker.Custom'>' is not accepted by Accepter from {u'bad_field': (Sanitizer to <type 'int'>, Accepter from <type 'int'>), u'd1': (Sanitizer to <type 'int'>, Accepter from <type 'int'>)}

        >>> customd1d2_tc = TypeChecker(Sanitizer(customd1d2_sanitizer), Accepter({
        ...     'd1': TypeChecker(Sanitizer(int),Accepter(int)),
        ...     'd2': TypeChecker(Sanitizer(int),Accepter(int))
        ... }))
        >>> customd1d2_tc(custom_msg)
        Traceback (most recent call last):
        ...
        TypeCheckerException: 'd1:42 d2:bla:<class 'typechecker.Custom'>' is not accepted by Accepter from {u'd2': (Sanitizer to <type 'int'>, Accepter from <type 'int'>), u'd1': (Sanitizer to <type 'int'>, Accepter from <type 'int'>)}
        """

        accepted = value is None  # value none is always accepted (default sanitized value)
        if not accepted:
            try:
                accepted = self.accepter(value)  # TODO : any new-style object can be read as a dictionnary... or we can access slots.
                # TODO : replace with contracts ?

            except Exception as e:
                raise TypeCheckerException("'{v}:{vt}' cannot be accepted by {a}\n              Reason: {e}".format(
                    v=value, vt=type(value), a=self.accepter, e=e
                ))

        if accepted:
            try:
                sanitized_value = self.sanitizer(value)
            except TypeError as te:
                raise TypeCheckerException("'{v}:{vt}' cannot be sanitized by {s}\n              Reason: {te}".format(
                    v=value, vt=type(value), s=self.sanitizer, te=te
                ))
        else:
            try:
                raise TypeCheckerException("'{v}:{vt}' is not accepted by {a}".format(
                    v=value, vt=type(value), a=self.accepter
                ))
            except UnicodeDecodeError:  # if we get an error decoding the value, we change the exception text
                raise TypeCheckerException("value of type {vt} is not accepted by {a}".format(
                    vt=type(value), a=self.accepter
                ))

        return sanitized_value

    def __repr__(self):
        return "({self.sanitizer}, {self.accepter})".format(**locals())

    def default(self):
        """
        Retrieves a default value based on the typeschema
        :param typeschema: the type schema
        :return: default value for that type

        Examples:
        >>> bool_ts = TypeChecker(Sanitizer(bool), Accepter(bool))
        >>> bool_ts.default()
        False

        >>> int_ts = TypeChecker(Sanitizer(int), Accepter(int))
        >>> int_ts.default()
        0

        >>> float_ts = TypeChecker(Sanitizer(float), Accepter(float))
        >>> float_ts.default()
        0.0

        >>> str_ts = TypeChecker(Sanitizer(str), Accepter(str))
        >>> str_ts.default()
        ''

        >>> array_ts = TypeChecker(Array(Sanitizer(bool)), Array(Accepter(bool)))
        >>> array_ts.default()
        []
        >>> array_ts = TypeChecker(Array(Sanitizer(int)), Array(Accepter(int)))
        >>> array_ts.default()
        []
        >>> array_ts = TypeChecker(Array(Sanitizer(float)), Array(Accepter(float)))
        >>> array_ts.default()
        []
        >>> array_ts = TypeChecker(Array(Sanitizer(str)), Array(Accepter(str)))
        >>> array_ts.default()
        []
        >>> array_ts = TypeChecker(Array(Sanitizer(float)), Array(Accepter(float)))
        >>> array_ts.default()
        []


        Examples with complex types
        >>> class Custom(object):
        ...     def __init__(self, d1=0, d2=''):
        ...         self.d1 = d1; self.d2 = d2
        ...     def __repr__(self):
        ...         return "d1:{d1} d2:{d2}".format(d1=self.d1, d2=self.d2)
        >>> custom_msg = Custom(42, d2='bla')

        >>> customd1_sanitizer = lambda x=None: Custom(d1=x.d1) if x else Custom(d1=1)
        >>> customd1_tc = TypeChecker(Sanitizer(customd1_sanitizer), Accepter({
        ...     'd1': TypeChecker(Sanitizer(int), Accepter(int))
        ... }))
        >>> customd1_tc.default()
        d1:1 d2:


        """
        return self.sanitizer()


# We need instance to determine field type
# TODO : use type hints instead of instantiation to determine types and sanitizers
def make_typechecker_from_prototype(inst, field_map=None):
    """
    Builds an Accepter from an object instance
    :param inst: the instance to introspect
    :param field_map: the mapping from python type to typecheck instance
    :return:
    """

    field_map = field_map or make_typechecker_from_prototype  # default field map is the trivial recursive one
    t = type(inst)
    if t in [bool, int, float, six.string_types]:
        # our stopping case is simple because of our chosen representation (python types representing python types)
        return TypeChecker(Sanitizer(t), Accepter(t))
    elif t is list and len(t) >1:
        subt = type(inst[0])  # getting the type of the first element
        return TypeChecker(Array(Sanitizer(subt)), Array(Accepter(t)))
    elif hasattr(t, '__dict__'):  # composed type with dict
        # TODO : check if this is actually used or even useful
        # we need to recurse on dict keys that are not builtin
        members = {
            f: field_map(type(ft))
            for f, ft in vars(type(inst)).items()
            if not f.startswith("__")
        }
        #TODO : FIX (copy from rostype implementation) and test...
        def sanitizer(**kwargs):
            return t(**{
                k: members.get(k)(v)  # we pass a subvalue to the sanitizer of the member type
                for k, v in kwargs
            })

        return TypeChecker(Sanitizer(sanitizer), Accepter(members))


# TODO : use type hints instead of instantiation
# def make_typechecker_from_class(cls, field_map=None):


def make_typechecker_field_optional(typechecker):
    """Builds a new type checker, which is the same as the type checker passed as argument, except that None is now accepted"""
    # copy on write, since multiple fields can share the same typechecker, but we want to mutate only this one
    return TypeChecker(typechecker.sanitizer, Any(Accepter(None), typechecker.accepter))



def make_typechecker_field_hidden(typechecker):
    """Builds a new type checker, which is the same as the type checker passed as argument, except that None is now accepted"""
    # copy on write, since multiple fields can share the same typechecker, but we want to mutate only this one
    return TypeChecker(typechecker.sanitizer, Accepter(None))


# TODO : function to modify a message type __init__ method
