# COPYRIGHT 2004-2005 DUMPLETON SOFTWARE CONSULTING PTY LIMITED

from mod_python import apache
from mod_python import util

# We can't use the "import" statement for "publisher"
# because of strange problems in mod_python module
# loader. Namely, if "import" is used and PythonHandler
# is defined elsewhere as "mod_python.publisher" and it
# gets loaded before this code, the "publisher" module
# can not then be found. Instead use the mod_python
# module loader itself as then it always works.

#from mod_python import publisher
publisher = apache.import_module("mod_python.publisher")

import os
import types
import string
import re
import sys

import cache
import config
import forms

_moduleCache = cache.ModuleCache()
_configCache = config.ConfigCache()


# Convenience method for loading a module based on its
# absolute path name.

def _import(req,file):

  # Files has to exist before we attempt to load it.

  if not os.path.exists(file):
    return None

  # Do not allow this actual code file to be imported.

  if file == __file__:
    return None

  # Attempt to load Python code module from cache.

  directory = os.path.dirname(file)
  name = os.path.splitext(os.path.basename(file))[0]

  module = _moduleCache.importModule(name,directory,req)

  return module


# Following provides authentication checks for a
# sequence of objects. For the time being, it uses the
# authentication routine that is included with
# mod_python.publisher.

def _authenticate(req,objects):

  realm,user,passwd = ("unknown",None,None)

  for object in objects:
    realm,user,passwd = publisher.process_auth(req,object,realm,user,passwd)


# Access to and traversal of objects is controlled by
# the following method. The method must be supplied a
# set of rules keyed by object type. In the rule which
# is specified for each type, three entries must be
# defined. These correspond to whether it is possible to
# traverse an object of that type, execute an object of
# that type, or access an object of that type. In order
# to be able to execute an object, the object must also
# be callable. Objects can also be blocked by a filter
# based on the actual name. The default filter provided
# blocks any name component which begins with a leading
# underscore.

def _default_filter(req,name,object):
  return name[:1] != '_'

def _resolve(req,object,parts,rules,filter=_default_filter):

  objects = [object]

  default = rules.get(None)

  # This method can be called with either "None" or a
  # list of path elements. If "None" is supplied then
  # simply apply the rules directly against the object
  # only.

  if parts is None:

    object_type = type(object)

    traverse,execute,access = rules.get(object_type,default)

  else:

    for i,part in enumerate(parts):

      # Block anything which fails the filter callback.

      if not filter(req,part,object):
	return (False,False,False,None)

      # Block everything when no such object exists.

      try:
	object = getattr(object,part)
	object_type = type(object)
      except AttributeError:
	return (False,False,False,None)

      # Extend list of traversed objects in the path.

      objects.append(object)

      # Apply rule set to the next object in the path.

      traverse,execute,access = rules.get(object_type,default)

      # Check for whether traversal is allowed needs to be
      # performed on all but the last object in the path.

      if i < (len(parts)-1):
	if not traverse:
	  return (False,False,False,None)

  # Even if the rule says that the last object is
  # potentially executable it doesn't necessarily mean
  # that it is. Thus need to check that it is in fact
  # callable and if not mark it as such.

  execute = execute and callable(object)

  # Also enforce a special rule that an object can only
  # be accessible if it is not traversable. In order to
  # publish a traversable object it therefore must be
  # executable.

  access = not traverse and access

  return (traverse,execute,access,objects)


# Following method determines the set of parameters
# that a callable object is able to accept or whether
# it accepts keyword arguments.

def _params(object):

  # If callable object doesn't take keyword argument
  # list then drop out arguments for which there is no
  # corresponding named parameter.

  fc = None

  if callable(object):
    object_type = type(object)

    if object_type is types.FunctionType:
      fc = object.func_code
      defaults = object.func_defaults
      expected = fc.co_varnames[0:fc.co_argcount]

    elif object_type is types.MethodType:
      fc = object.im_func.func_code
      defaults = object.im_func.func_defaults
      expected = fc.co_varnames[1:fc.co_argcount]

    elif object_type is types.ClassType:
      fc = object.__init__.im_func.func_code
      defaults = object.__init__.im_func.func_defaults
      expected = fc.co_varnames[1:fc.co_argcount]

    elif hasattr(object,"__call__"):
      fc = object.__call__.im_func.func_code
      defaults = object.__call__.im_func.func_defaults
      expected = fc.co_varnames[1:fc.co_argcount]

    elif hasattr(object,"func_code"):
      fc = object.func_code
      defaults = object.func_defaults
      expected = fc.co_varnames[0:fc.co_argcount]

    elif hasattr(object,"im_func"):
      fc = object.im_func.func_code
      defaults = object.im_func.func_defaults
      expected = fc.co_varnames[1:fc.co_argcount]

  if fc is None:
    return (apache.HTTP_INTERNAL_SERVER_ERROR,None,None,None)

  if defaults is None:
    defaults = []

  return (apache.OK,fc.co_flags,expected,defaults)


# Following executes a callable object. Any form
# parameters are automatically decoded and as
# appropriate are passed to the callable object when it
# is executed. The "req" parameter is always treated
# specially, with the request object being passed in
# using that parameter.

def _execute(req,object):

  args = {}

  # Determine names of parameters expected by callable
  # object and whether it also supports variable argument
  # list or keyword argument list.

  status,flags,expected,defaults = _params(object)

  if status != apache.OK:
    raise apache.SERVER_RETURN, status

  # Decode form parameters if appropriate content type
  # and callable object specifies parameters other than
  # that for request object.

  if not hasattr(req,"form") and (flags & 0x08 or \
      (len(expected) == 1 and not "req" in expected) or len(expected)):

    if not req.headers_in.has_key("content-type"):
      content_type = "application/x-www-form-urlencoded"
    else:   
      content_type = req.headers_in["content-type"]

    if content_type == "application/x-www-form-urlencoded" or \
        content_type[:10] == "multipart/":

      req.form = util.FieldStorage(req,keep_blank_values=1)

  if hasattr(req,"form"):

    # Merge form data into list of possible arguments.
    # Convert the single item lists back into values.

    for field in req.form.list:
      if field.filename: 
	value = field
      else:
	value = field.value

      if args.has_key(field.name):
	args[field.name].append(value)
      else:
	args[field.name] = [value]

    for arg in args.keys():
      if type(args[arg]) == types.ListType:
	if len(args[arg]) == 1:
	  args[arg] = args[arg][0]

    # Some strange forms can result in fields where the
    # key value is None. Wipe this out just in case this
    # happens as can cause problems later.

    if args.has_key(None):
      del args[None]

    # Magic code which interprets certain naming
    # conventions in argument names and converts sets of
    # arguments into lists and dictionaries. Code borrowed
    # from FormEncode/Validator which can be obtained from
    # "http://formencode.org/".

    advanced = True

    options = req.get_options()
    if options.has_key("VampireStructuredForms"):
      value = options["VampireStructuredForms"]
      if value in ["Off","off"]:
	advanced = False

    if advanced:
      args = forms.variable_decode(args)

  # Add request object set of input form parameters.

  args["req"] = req

  # If callable object doesn't support keyword argument
  # list, filter out form parameters that don't match
  # any input parameter.

  if not flags & 0x08:
    for name in args.keys():
      if name not in expected:
	del args[name]

  # Execute as callable object.

  return object(**args)


# Following is used to format the response from a
# publisher method. This yields slightly different
# results to mod_python.publisher in that a None object
# which is returned by a method does not result in a 500
# error, instead an empty page would be returned.

def _flush(req,result):

  if result is not None:
    result = str(result)
  else:
    result = ""

  # The same type of check for HTML is used here as is
  # used in the mod_python.publisher module. This is not
  # the most reliable of checks that could be made as
  # modern HTML which follows some sort of standard will
  # not begin with "<html>". Thus end up having to fall
  # back to searching the whole text for "</". This will
  # work for HTML, but may also cause false positives
  # in plain text where somewhere in the content that
  # strings appears somewhere.

  if not req._content_type_set:
    if string.lower(string.strip(result[:100])[:6]) == '<html>' \
	or string.find(result,'</') > 0:
      req.content_type = 'text/html'
    else:
      req.content_type = 'text/plain'
    req.send_http_header()

  req.write(result)

  return apache.OK


# Define the basic Vampire content handler. Whereas the
# standard mod_python handler only allows one handler
# for a directory and everything under it, this handler
# allows distinct handlers against each resource in a
# directory. Multiple handlers can also be associated
# with the one resource where the resource can be
# represented in multiple data formats. First need to
# define the traversal rules, although they aren't
# strictly required yet as don't provide a traversal
# mechanism for handlers, although do use it to check
# that where a handler is an object that it can be used.

_handler_rules = {}

# Add in the default rule. This effectively means that
# anything that is left and that can be executed, will
# be able to be used. It wasn't actually necessary to
# even add rules for functions, methods and old style
# class instances as is done below, but do it so that
# everything is explicit.

_handler_rules[None] = (False,True,False)

# For all of the Python builtin types, mark them as
# not being able to be traversed, executed or accessed.

for t in types.__dict__.values():
  if type(t) is types.TypeType:
    _handler_rules[t] = (False,False,False)

# Instances of any old style classes are marked as being
# potentially executable.

_handler_rules.update({
  types.InstanceType: (False,True,False),
})

# Globally defined functions and methods of a class are
# marked as potentially executable.

_handler_rules.update({
  types.FunctionType: (False,True,False),
  types.MethodType:   (False,True,False),
})

# Now for the actual handler function which implements
# the publisher functionality.

def _handler(req):

  # Create a working area in request object if it
  # doesn't exist already.

  if not hasattr(req,"vampire"):
    req.vampire = {}

  # Record in request object which handler is servicing
  # the request. This can be used by a handler to
  # accomodate being able to be called as a handler or
  # publisher type method.

  req.vampire["handler"] = "vampire::handler"

  # Translate a request against a directory to a request
  # against a specified index file.

  if req.path_info == "" and os.path.isdir(req.filename):
    options = req.get_options()
    if options.has_key("VampireDirectoryIndex"):
      value = options["VampireDirectoryIndex"]
      if value != ".":
        if req.args:
	  value = "%s?%s" % (value,req.args)
	if hasattr(req,"internal_redirect"):
	  req.internal_redirect(req.uri+value)
	else:
	  req.headers_out["location"] = "%s" % value
	  req.status = apache.HTTP_MOVED_TEMPORARILY
	return apache.OK

  # Determine type of file based on extension.

  stub,extn = os.path.splitext(req.filename)

  # Forbid requests against Python code files or
  # anything which may be generated from them.

  if extn in [".py",".pyc",".pyo"]:
    if os.path.exists(req.filename):
      return apache.HTTP_NOT_FOUND

  # Determine name of the content handler to be used.

  if extn != "":
    method = "handler_%s" % extn[1:]
  else:
    method = "handler"

  # Search for handler in associated python code.

  file = stub + ".py"
  module = _import(req,file)

  # If we have already found a valid module, first check
  # to see if it provides an appropriate handler. If it
  # does, only then check try and authenticate actual
  # access.

  objects = None
  rules = _handler_rules

  if module:
    if not hasattr(module,"__handle__") or extn in module.__handle__:
      traverse,execute,access,objects = _resolve(req,module,[method],rules)

  # Look for a default handler if no dedicated handler.

  if objects is None:
    options = req.get_options()
    if options.has_key("VampireDefaultHandlers"):
      if options["VampireDefaultHandlers"] in ["On","on"]:
	file = ".vampire"
        if options.has_key("VampireHandlersConfig"):
	  file = options["VampireHandlersConfig"]
	config = _configCache.loadConfig(req,file)
	section = "Handlers"
        if options.has_key("VampireHandlersSection"):
	  section = options["VampireHandlersSection"]
	if config.has_section(section):
	  file = None
	  if config.has_option(section,method):
	    file = config.get(section,method)
	  if file != None:
	    if os.path.splitext(file)[1] != ".py":
	      return apache.HTTP_INTERNAL_SERVER_ERROR
	    module = _import(req,file)
	    if module:
	      traverse,execute,access,objects = _resolve(req,
	          module,[method],rules)

  # Return control to Apache if we were unable to find
  # an appropriate handler to execute.

  if objects is None:
    return apache.DECLINED

  # Only now authenticate all the objects that had to be
  # traversed to reach the target handler. By doing it at
  # this point, we can pass back control to Apache when
  # we can't handle the request without errornously
  # triggering any unecessary authentication first.

  _authenticate(req,objects)

  # Execute the content handler which was found.

  result = _execute(req,objects[-1])

  # To try and make standard content handlers and
  # publisher style handlers interchangeable, allow a
  # return value of "None" to be interchangeable with
  # returning "apache.OK".

  if result is None:
    return apache.OK

  return result


# Following provides an alternate implementation of the
# mod_python.publisher module. It fixes various bugs in
# the original. First need to define the traversal rules
# to be used when resolving the function path. Note that
# the rules are just as loose as mod_python.publisher
# and thus if one isn't careful one can expose the fact
# that Python is used because of default rules all
# objects have for conversion to strings. Thus need to
# prefix names with underscore if you don't want them
# exposed.

_publisher_rules = {}

# For all types defined by Python itself, first mark
# them as not being able to be traversed or executed,
# but allow them to be accessed.

for t in types.__dict__.values():
  if type(t) is types.TypeType:
    _publisher_rules[t] = (False,False,True)

# Modules are marked as not being able to be traversed,
# executable or accessible.

_publisher_rules.update({
  types.ModuleType: (False,False,False),
})

# New and old style classes are marked as not being able
# to be traversed, executable or accessible.

_publisher_rules.update({
  types.ClassType: (False,False,False),
  types.TypeType: (False,False,False),
})

# Instances of any old style classes are marked as being
# traversable and potentially executable.

_publisher_rules.update({
  types.InstanceType: (True,True,False),
})

# Globally defined functions and methods of a class are
# executable, but cannot be traversed or accessed.

_publisher_rules.update({
  types.FunctionType: (False,True,False),
  types.MethodType:   (False,True,False),
})

# Builtin functions are marked as not being able to be
# traversed, executed or accessed. They are not allowed
# to be executable as they don't have named parameters.

_publisher_rules.update({
  types.BuiltinFunctionType: (False,False,False),
})

# In practice what is left are instances of new style
# classes and classes implemented in a C extension
# module. These are defined as being traversable and
# potentially executable by way of application of a
# default rule.

_publisher_rules[None] = (True,True,False)

# Now for the actual handler function which implements
# the publisher functionality.

def _publisher(req):

  # Create a working area in request object if it
  # doesn't exist already.

  if not hasattr(req,"vampire"):
    req.vampire = {}

  req.vampire["handler"] = "vampire::publisher"

  # The mod_python.publisher code only allows GET and
  # POST. Don't know why it couldn't permit other types
  # of requests, but then it is mean't to be simplistic.

  if hasattr(req,"allow_methods"):
    req.allow_methods(["GET","POST"])

  if req.method not in ["GET","POST"]:
    raise apache.SERVER_RETURN, apache.HTTP_METHOD_NOT_ALLOWED

  # Derive the name of the actual module which will be
  # loaded. In mod_python.publisher you can't actually
  # have a code file name which has an embedded '.' in
  # it except for that used by the extension. This is
  # because the standard Python module import system which
  # is used will think that you are importing a submodule
  # of a package. In this code, because the standard Python
  # module import system isn't used and the actual file
  # is open directly by name, a embedded '.' besides that
  # used for the extension will technically work.

  path,module_name =  os.path.split(req.filename)

  # If the request is against the the directory itself,
  # fallback to looking for the "index" module.

  if not module_name:  
    module_name = "index"

  # Now need to strip off any special extension which
  # was used to trigger this handler in the first place.
  # Note though that "req.get_addhandler_exts()" and
  # "req.extension" only exist in mod_python 3.X. If
  # older version of mod_python is used, only the ".py"
  # extension is supported when the AddHandler directive
  # is used as there is no easy way of detecting what
  # the extension was that was used with AddHandler.

  suffixes = ["py"]

  if hasattr(req,"get_addhandler_exts"):
    suffixes = req.get_addhandler_exts().split()
    if req.extension:
      suffixes.append(req.extension[1:])

  if suffixes:
    exp = "\\." + "$|\\.".join(suffixes) + "$"
    suff_matcher = re.compile(exp)
    module_name = suff_matcher.sub("",module_name)

  # Next need to determine the traversal path for the
  # function which will be called from the "path_info".
  # The mod_python.publisher module is actually a bit
  # sloppy as far as processing of this path in that it
  # allows '.' to be used instead of '/'. In this code
  # we don't do that as the ability to use '.' is an
  # indicator of how the system is implemented.

  func_path = ""

  if req.path_info:
    func_path = req.path_info[1:]
    if func_path[-1:] == "/":
      func_path = func_path[:-1]

  # Now import the module itself. This will first try
  # looking for "/path/<module_name>.py". If this does
  # not actually work, try fallback of using the "index"
  # module, ie., look for "/path/index.py". In doing
  # this, the "func_path" gets adjusted so the lead part
  # is what "module_name" was set to. This is a bit
  # different to mod_python.publisher 2.7.11 and 3.1.14
  # which both have a bug in them which means the
  # adjustment of "func_path" is not done which thus
  # prevents traversal into an object when falling back
  # on "index" module. The original mod_python.publisher
  # also has a bug whereby it can fallback to default
  # "index.py" file when it should if genuine import
  # error occurs when loading first module. This is
  # because it doesn't properly distinguish case where
  # module simply did not exist.

  file = path + '/' + module_name + ".py"
  module = _import(req,file)

  if not module:
    if func_path:
      func_path = module_name + '/' + func_path
    else:
      func_path = module_name
    module_name = "index" 
    file = path + '/' + module_name + ".py"
    module = _import(req,file)

    if not module:
      raise apache.SERVER_RETURN, apache.HTTP_NOT_FOUND

  # Default to looking for the 'index' function if no
  # function path definition was supplied.

  if not func_path:
    func_path = "index"

  # Now resolve the path to identify target object,
  # applying the publisher rule set in the process.

  rules = _publisher_rules
  parts = func_path.split('/')

  traverse,execute,access,objects = _resolve(req,module,parts,rules)

  # Execute callable object or translate object into
  # response as appropriate.

  if objects is not None:

    _authenticate(req,objects)

    if execute:
      result = _execute(req,objects[-1])

      return _flush(req,result)

    elif access:
      return _flush(req,objects[-1])

  raise apache.SERVER_RETURN, apache.HTTP_NOT_FOUND


# Define a generic handler for directives other
# than the PythonHandler. This will consult the
# configuration file as to the appropriate
# module to load and then execute.

def _select(req,name):

  # Create a working area in request object if it
  # doesn't exist already.

  if not hasattr(req,"vampire"):
    req.vampire = {}

  # Try and find entry in appropriate config.

  options = req.get_options()

  file = ".vampire"
  if options.has_key("VampireHandlersConfig"):
    file = options["VampireHandlersConfig"]

  config = _configCache.loadConfig(req,file)

  section = "Handlers"
  if options.has_key("VampireHandlersSection"):
    section = options["VampireHandlersSection"]

  handler = None

  if config.has_section(section):
    if config.has_option(section,name):
      handler = config.get(section,name)

  # If there is no entry or it is empty, skip it.

  if not handler:
    return apache.OK

  # Ensure handler is a Python module file.

  if os.path.splitext(handler)[1] != ".py":
    return apache.HTTP_INTERNAL_SERVER_ERROR

  # The handler is supposed to be the actual
  # file name of the module to load. The actual
  # handler within it must be matching name for
  # the directive, it can't be something else.

  directory = os.path.dirname(handler)
  stub = os.path.splitext(os.path.basename(handler))[0]

  module = _moduleCache.importModule(stub,directory,req)

  # Determine the appropriate content handler.

  function = None

  if hasattr(module,name):
    function = getattr(module,name)

  # Were we able to find a function to execute.

  if function == None:
    return apache.OK

  # Execute the actual handler function.

  result = function(req)

  if result is None:
    return apache.OK

  return result


class Handler:

  def __init__(self,object):
    self.__object = object

  def __call__(self,req):

    # Check to see if this is actually being executed
    # from outside of Vampire. In that case, we need to
    # determine the appropriate value for "path_info"
    # ourselves based on where handler was defined.

    if not hasattr(req,"vampire"):

      handler_root = None

      if hasattr(req,"hlist"):
	# In mod_python 3.X have the req.hlist member.
	handler_root = req.hlist.directory
      elif hasattr(req,"get_dirs"):
	# In mod_python 2.X have the req.get_dirs() method.
	handler_root = req.get_dirs()["PythonHandler"]

      if handler_root is None:
	raise apache.SERVER_RETURN, apache.HTTP_INTERNAL_SERVER_ERROR

      length = len(req.filename) - len(handler_root)

      path_info = "/"

      if length != 0:
	path_info += req.filename[-length:]

      req.vampire = {}

    else:
      path_info = req.path_info

    # First need to determine the traversal path for the
    # function which will be called from the "path_info".

    func_path = ""

    if path_info:
      func_path = path_info[1:]
    if func_path[-1:] == "/":
      func_path = func_path[:-1]

    # Now resolve the path to identify target object.

    if func_path:
      parts = func_path.split('/')
    else:
      parts = None

    rules = _handler_rules

    traverse,execute,access,objects = _resolve(req,self.__object,parts,rules)

    # Return control to Apache if we were unable to find
    # an appropriate handler to execute.

    if objects is None:
      return apache.DECLINED

    # Only now authenticate all the objects that had to be
    # traversed to reach the target handler. By doing it at
    # this point, we can pass back control to Apache when
    # we can't handle the request without errornously
    # triggering any unecessary authentication first.

    _authenticate(req,objects)

    # Execute the content handler which was found.

    result = _execute(req,objects[-1])

    # To try and make standard content handlers and
    # publisher style handlers interchangeable, allow a
    # return value of "None" to be interchangeable with
    # returning "apache.OK".

    if result is None:
      return apache.OK

    return result


class Publisher:

  def __init__(self,object):
    self.__object = object

  def __call__(self,req):

    # Check to see if this is actually being executed
    # from outside of Vampire. In that case, we need to
    # determine the appropriate value for "path_info"
    # ourselves based on where handler was defined.

    if not hasattr(req,"vampire"):

      handler_root = None

      if hasattr(req,"hlist"):
	# In mod_python 3.X have the req.hlist member.
	handler_root = req.hlist.directory
      elif hasattr(req,"get_dirs"):
	# In mod_python 2.X have the req.get_dirs() method.
	handler_root = req.get_dirs()["PythonHandler"]

      if handler_root is None:
	raise apache.SERVER_RETURN, apache.HTTP_INTERNAL_SERVER_ERROR

      length = len(req.filename) - len(handler_root)

      path_info = "/"

      if length != 0:
	path_info += req.filename[-length:]

      req.vampire = {}

    else:
      path_info = req.path_info

    # Now need to determine the traversal path for the
    # function which will be called from the "path_info".

    func_path = ""

    if path_info:
      func_path = path_info[1:]
    if func_path[-1:] == "/":
      func_path = func_path[:-1]

    # Now resolve the path to identify target object.

    if func_path:
      parts = func_path.split('/')
    else:
      parts = None

    rules = _publisher_rules

    traverse,execute,access,objects = _resolve(req,self.__object,parts,rules)

    # Execute callable object or translate object into
    # response as appropriate.

    if objects is not None:

      _authenticate(req,objects)

      if execute:
	req.vampire["handler"] = "vampire::publisher"

	result = _execute(req,objects[-1])

	return _flush(req,result)

      elif access:
	return _flush(req,objects[-1])

    raise apache.SERVER_RETURN, apache.HTTP_NOT_FOUND


class PathInfo:

  def __init__(self,callback,name="path",path=[]):

    self.__callback = callback
    self.__name = name
    self.__path = path

  def __call__(self,req,**args):

    status,flags,expected,defaults = _params(self.__callback)

    if status != apache.OK:
      raise apache.SERVER_RETURN, status

    args[self.__name] = '/'.join([""]+self.__path)
    args["req"] = req

    if not flags & 0x08:
      for name in args.keys():
        if name not in expected:
          del args[name]

    return self.__callback(**args)

  def __getattr__(self,name):

    if name[:1] != '_':
      return PathInfo(self.__callback,self.__name,self.__path+[name])

    raise AttributeError(name)


class PathArgs:

  def __init__(self,callback,parent=None,path=[]):

    self.__callback = callback
    self.__path = path

    if parent is not None:
      self.__expected = parent.__expected
      self.__minargs = parent.__minargs
      self.__maxargs = parent.__maxargs
      self.__varargs = parent.__varargs
    else:
      self.__expected = None
      self.__minargs = None
      self.__maxargs = None
      self.__varargs = None

  def __setup(self):

    status,flags,expected,defaults = _params(self.__callback)

    if status != apache.OK:
      raise apache.SERVER_RETURN, status

    self.__expected = expected
    self.__maxargs = len(expected)
    self.__minargs = self.__maxargs - len(defaults)
    self.__varargs = (flags & 0x04)

  def __call__(self,req):

    if self.__expected is None:
      self.__setup()

    if self.__expected[:1] == ("req",):

      if len(self.__path) < (self.__minargs-1):
	raise apache.SERVER_RETURN, apache.HTTP_NOT_FOUND

      return self.__callback(req,*self.__path)

    else:

      if len(self.__path) < self.__minargs:
	raise apache.SERVER_RETURN, apache.HTTP_NOT_FOUND

      return self.__callback(*self.__path)

  def __getattr__(self,name):

    if name[:1] != '_':

      if self.__expected is None:
        self.__setup()

      if not self.__varargs:

        if self.__expected[:1] == ("req",) and \
	    len(self.__path) == (self.__maxargs-1):
	  raise apache.SERVER_RETURN, apache.HTTP_NOT_FOUND

	elif len(self.__path) == self.__maxargs:
	  raise apache.SERVER_RETURN, apache.HTTP_NOT_FOUND

      path = self.__path + [name]
      return PathArgs(self.__callback,self,path)

    raise AttributeError(name)
