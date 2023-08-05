from __future__ import absolute_import, division, print_function

"""
pyros_msgs.opt_as_array is a module that interprets arrays as optional fields in a message.

This is useful if you have an existing ros message type, and want to allow some field to not have any defined value :
An empty array will represent that, but it might be ambiguous...

"""


from .opt_as_array import duck_punch
