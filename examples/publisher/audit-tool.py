# This file exhibits various possible types which can be
# constructed in Python for the purpose of showing in
# what way they are accessible using vampire::publisher.
#
# The rules are similar to mod_python.publisher which
# means that it is possible to access objects such as
# file objects, generators, xrange object etc. Doing so
# will return a default string generated by Python and
# which reveals implementation details. Thus you still
# need to ensure that objects such as these that should
# not be visible be prefixed with an underscore to hide
# them.
#
# The only objects which are traversable are instances
# of old style and new style classes, with the exception
# of any new style class which is a Python builtin type.
# Although mod_python.publisher accepts the URL "a.b"
# and "a/b" as the same thing, vampire::publisher only
# accepts the "a/b" form, ie., where object names within
# a traversal path are separated by a "/".
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

# FileType: Accessible.
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

# StringType: Accessible.
type_string_html = "<html<p>1</p></html>"

# TupleType: Accessible.
type_tuple = (1,)

# UnicodeType: Accessible.
type_unicode = u"1"

# BuiltinFunctionType: Forbidden.
type_builtin_function = globals

# FunctionType: Callable.
def type_function(): return "1"

# GeneratorType: Accessible.
def type_generator(): yield 1
type_generator = type_generator()

# XRangeType: Accessible.
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
type_instance = type_class()

# Type of InstanceType: Accessible (If Type is Accessible)
#   type_instance/member --> "type_class.member"

# MethodType of InstanceType: Callable
#   type_instance/method --> "type_class.method()"

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

# Instance of <new style class>: Traversable/Callable.
#   type_new_style_class_instance --> "type_new_style_class.__call__()"
type_new_style_class_instance = type_new_style_class()

# Type of <new style class>: Accessible (If Type is Accessible)
#   type_new_style_class_instance/member --> "type_new_style_class.member"

# MethodType of <new style class>: Callable
#   type_new_style_class_instance/method --> "type_new_style_class.method()"



from mod_python import apache

import os
import cgi
import types

import vampire

from vampire.lookup import _resolve,_publisher_rules

_index = """
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
<form method="GET" action="%(action)s">
Module:
<input size=50 name="name" value="%(module)s" />
<input type="submit" value="Browse" name="action" />
</form>
</body>
</p>
</html>
"""

def index(req):

  directory = '/'.join((len(req.path_info.split('/'))-1)*[".."])
  module = os.path.splitext(os.path.split(req.filename)[1])[0]

  if not directory:
    directory = '.'

  action = "%s/%s/browse" % (directory,module)

  return _index % { "action": action, "module": module }

def browse(req,name="",object="",**kw):

  if req.vampire["handler"] != "vampire::publisher":
    return apache.HTTP_NOT_IMPLEMENTED

  directory = '/'.join((len(req.path_info.split('/'))-1)*[".."])
  module = os.path.splitext(os.path.split(req.filename)[1])[0]

  if not directory:
    directory = '.'

  action = "%s/%s/browse" % (directory,module)

  rules = _publisher_rules

  directory = os.path.dirname(req.filename)

  try:
    target = vampire.importModule(os.path.split(name)[1],directory)
  except OSError:
    value = os.path.split(req.uri)[0]
    req.headers_out["location"] = "%s" % value
    req.status = apache.HTTP_MOVED_TEMPORARILY
    return apache.HTTP_NOT_FOUND

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
    status,traverse,execute,access,subinstance = _resolve(
        req,root,parts,rules)

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
        req.write("<a href='%s"%action)
        req.write("?name=%s&object=%s'>"%(name,subobject))
        req.write("BROWSE")
        req.write("</a>")

      if execute:
        req.write("&nbsp;")
        url = action + '/../' + subobject
        req.write("<a href='%s'>" % url)
        req.write("EXEC")
        req.write("</a>")

      if access:
        req.write("&nbsp;")
        url = action + '/../' + subobject
        req.write("<a href='%s'>" % url)
        req.write("VIEW")
        req.write("</a>")

      req.write("</td>\n")

      req.write("</tr>\n")

  req.write("</table>\n")
  req.write("</body></html>\n")
