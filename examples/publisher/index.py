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
#
# If this page is accessed, it will give access to an
# auditing tool which will allow you to view how the
# rules apply to the data contained with the module. The
# tool uses the exact same code as vampire::publisher
# itself uses to determine what is accessible so should
# be an accurate reflection of reality.

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
type_generator = type_generator()

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



from mod_python import apache

import os
import cgi
import types

import vampire

from vampire.lookup import _resolve,_params,_publisher_rules

index = """
<html>
<head>
<title>Publisher Auditing Tool</title>
</head>
<body>
<h1>Vampire Auditing Tool</h1>
<p>
This tool can be used to show you exactly what you are exposing of
your web site to the outside world when you are using the
vampire::publisher extension. You may be suprised at what you find. :-)
</p>
<p>
You should now give the name of the module you wish to inspect. If the
module is in a subdirectory, list the name using slash notation and not as
dot as is the convention for Python. For example enter in "subdir/module".
</p>
<p>
For a type object, selecting "VIEW" will show you what value would
be returned when accessing that object. For a callable object, selecting
"EXEC" will trigger a call of the object. In doing this though, it will
be called with no input parameters. Selecting "BROWSE" will allow you
to traverse into objects which support such behaviour.
</p>
<p>
<form method="GET" action="browse">
Module:
<input size=50 name="name" value="index" />
<input type="submit" value="Browse" name="action" />
</form>
</body>
</p>
</html>
"""

def browse(req,name="",object="",**kw):

  if req.vampire["handler"] != "vampire::publisher":
    return apache.HTTP_NOT_IMPLEMENTED

  MODULE = os.path.splitext(os.path.split(req.filename)[1])[0]

  rules = _publisher_rules

  directory = os.path.dirname(req.filename)

  target = vampire.importModule(os.path.split(name)[1],directory)

  root = target

  req.content_type = "text/html"
  req.send_http_header()
  req.write("<html><body>\n")

  if object != "":
    for element in object.split('/'):
      target = getattr(target,element)

  subobjects = dir(target)
  subobjects.sort()

  req.write("<table>\n")

  for key in subobjects:
    if object != "":
      subobject = object + "/" + key
    else:
      subobject = key

    req.write("<tr>\n")

    req.write("<td>\n")
    req.write("<p>\n")
    req.write(cgi.escape(subobject))
    req.write("</p>\n")
    req.write("</td>\n")

    subinstance = None
    typestring = ""
    if hasattr(target,key):
      subinstance = getattr(target,key) 
      typestring = cgi.escape(str(type(subinstance)))

    req.write("<td>\n")
    req.write("<p>%s</p>\n" % typestring)
    req.write("</td>\n")

    parts = subobject.split('/')
    traverse,execute,access,subinstance = _resolve(req,root,parts,rules)

    if not traverse and not execute and not access:
      req.write("<td>\n")
      req.write("DENY")
      req.write("</td>\n")

      req.write("<td>\n")
      req.write("</td>\n")

    else:
      req.write("<td>\n")
      if execute:
	req.write("CALL")
      else:
	req.write("TYPE")
      req.write("</td>\n")

      req.write("<td>\n")

      if traverse:
	req.write("&nbsp;")
	req.write("<a href='%s"%MODULE)
	req.write("?name=%s&object=%s'>"%(name,subobject))
	req.write("BROWSE")
	req.write("</a>")

      if execute:
	req.write("&nbsp;")
	url = name + '/' + subobject
	req.write("<a href='%s'>" % url)
	req.write("EXEC")
	req.write("</a>")

      if access:
	req.write("&nbsp;")
	url = name + '/' + subobject
	req.write("<a href='%s'>" % url)
	req.write("VIEW")
	req.write("</a>")

      req.write("</td>\n")

      req.write("</tr>\n")

  req.write("</table>\n")
  req.write("</body></html>\n")
