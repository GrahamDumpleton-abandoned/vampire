# This file exhibits various possible types which can be
# constructed in Python for the purpose of showing in
# what way they are accessible using vampire::publisher.
# The rules are not the same as for mod_python.publisher.
#
# Where access is against a callable object, the same
# rules for accessibility are applied to the result of
# calling the object. Thus, a result of a call is not
# blindly converted to a string.
#
# The only objects which are traversable are instances
# of old style and new style classes, with the exception
# of any new style class which is a Python builtin type.
# Although mod_python.publisher accepts the URL "a.b"
# and "a/b" as the same thing, vampire::publisher only
# accepts the "a/b" form, ie., where object names within
# a traversal path are separated by a "/".
#
# Note that anything that begins with an underscore is
# not accessible regardless of what it is. Although some
# types not prefixed with an underscore will not be
# accessible either, it is always good practice to
# prefix anything you don't intend to be accessible with
# an underscore.
#
# If something isn't shown here, access to it is likely
# forbidden.

# Hidden.
_hidden = None

# BoolType: Accessible.
type_bool = True

# BufferType: Accessible.
type_buffer = buffer("0123456789",2,6)

# ComplexType: Accessible.
type_complex = 1j

# DictType: Accessible.
type_dict = { "a": 1 }

# FileType: Forbidden.
from sys import stdout as type_file

# FloatType: Accessible.
type_float = 1.1

# IntType: Accessible.
type_int = 1

# ListType: Accessible.
type_list = [1]

# LongType: Accessible.
type_long = 1

# ModuleType: Forbidden.
import os

# NoneType: Accessible.
#   type_none --> ""
type_none = None

# StringType: Accessible.
type_string = "1"

# TupleType: Accessible.
type_tuple = (1,)

# UnicodeType: Accessible.
type_unicode = u"1"

# BuiltinFunctionType: Forbidden.
type_builtin_function = globals

# FunctionType: Callable.
def type_function(): return "1"

# GeneratorType: Forbidden.
def type_generator(): yield 1

# XRangeType: Forbidden.
type_xrange = xrange(0,10)

# ClassType: Forbidden.
class type_class:
  def __init__(self):
    self.member = "type_class.member"
  def method(self):
    return "type_class.method()"
  def __call__(self):
    return "type_class.__call__()"

# InstanceType: Traversable/Callable.
#   type_instance --> "type_class.__call__()"
#   type_instance/member --> "type_class.member"
#   type_instance/method --> "type_class.method()"
type_instance = type_class()

# MethodType: Callable.
#   type_method --> "type_class.method"
type_method = type_instance.method

# <new style class>: Forbidden.
class type_new_style_class(object):
  def __init__(self):
    self.member = "type_new_style_class.member"
  def method(self):
    return "type_new_style_class.method()"
  def __call__(self):
    return "type_new_style_class.__call__()"

# <new style class instance: Traversable/Callable.
#   type_new_style_class_instance --> "type_new_style_class.__call__()"
#   type_new_style_class_instance/member --> "type_new_style_class.member"
#   type_new_style_class_instance/method --> "type_new_style_class.method()"
type_new_style_class_instance = type_new_style_class()
