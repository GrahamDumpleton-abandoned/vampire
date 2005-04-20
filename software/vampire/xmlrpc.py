# COPYRIGHT 2004-2005 DUMPLETON SOFTWARE CONSULTING PTY LIMITED

from mod_python import apache

from lookup import _resolve, _authenticate, _params

import xmlrpclib
import types
import sys

def serviceRequest(req,callback):

  if req.method != "POST":
    raise apache.SERVER_RETURN, apache.HTTP_METHOD_NOT_ALLOWED

  if not req.headers_in.has_key("content-type") \
      or req.headers_in["content-type"] != "text/xml":
    raise apache.SERVER_RETURN, apache.HTTP_BAD_REQUEST

  content = req.read(int(req.headers_in["content-length"]))

  params,method = xmlrpclib.loads(content)

  try:
    response = callback(req,method,params)
    response = (response,)
    response = xmlrpclib.dumps(response,methodresponse=1)
  except apache.SERVER_RETURN:
    raise
  except xmlrpclib.Fault,fault:
    response = xmlrpclib.dumps(fault)
  except:
    response = xmlrpclib.dumps(
      xmlrpclib.Fault(1,"%s:%s" % (sys.exc_type,sys.exc_value)))

  req.content_type = "text/xml"

  req.headers_out['Content-Length'] = str(len(response)) 

  req.headers_out['Pragma'] = 'no-cache'
  req.headers_out['Cache-Control'] = 'no-cache'
  req.headers_out['Expires'] = '-1'

  req.send_http_header()

  req.write(response)


# Following provides an XML-RPC server implementation
# which allows traversal of objects in order to resolve
# a method. First need to define the traversal rules to
# be used when resolving the method path. If something
# should not be exposed, it should be prefixed with an
# underscore.

_xmlrpc_rules = {}

# For all types defined by Python itself, first mark
# them as not being able to be traversed or executed,
# but allow them to be accessed. Allowing access is a
# short cut so that the value of a basic data type can
# be returned without having to wrap access to it in a
# method. If a basic data type can't be marshalled as
# XML-RPC data, it will fail at that point.

for t in types.__dict__.values():
  if type(t) is types.TypeType:
    _xmlrpc_rules[t] = (False,False,True)

# Although module and class types can't be marshalled
# ensure that no attempt is even made to do so by
# explicitly blocking access to them.

_xmlrpc_rules.update({
  types.ModuleType: (False,False,False),
  types.ClassType: (False,False,False),
  types.TypeType: (False,False,False),
})

# Instances of any old style classes are marked as being
# traversable and potentially executable.

_xmlrpc_rules.update({
  types.InstanceType: (True,True,False),
})

# Globally defined functions, builtin functions and
# methods of a class are executable, but cannot be
# traversed or accessed.

_xmlrpc_rules.update({
  types.FunctionType: (False,True,False),
  types.MethodType:   (False,True,False),
  types.BuiltinFunctionType: (False,True,False),
})

# In practice what is left are instances of new style
# classes and classes implemented in a C extension
# module. These are defined as being traversable and
# potentially executable by way of application of a
# default rule.

_xmlrpc_rules[None] = (True,True,False)

# Now for the service object which processes the XML-RPC
# request and dispatches the call against the target.

class Service:

  def __init__(self,object):
    self.__object = object

  def _dispatch(self,req,method,params):

    # Now resolve the path to identify target object.

    parts = method.split('.')

    rules = _xmlrpc_rules

    status,traverse,execute,access,objects = _resolve(
        req,self.__object,parts,rules)

    req.vampire["objects"].extend(objects)

    _authenticate(req)

    # Execute callable object if possible.

    if status == apache.OK:

      if execute:
	req.vampire["handler"] = "vampire::xmlrpc"

	target = objects[-1]

        if type(target) == types.BuiltinFunctionType:
	  return target(*params)

	else:
	  status,flags,expected,defaults = _params(target)

	  if status != apache.OK:
	    raise xmlrpclib.Fault(1,"Method Unavailble : %s" % method)

	  if expected[:1] == ("req",):
	    return target(req,*params)

	  return target(*params)

      elif access:
	return objects[-1]

    raise xmlrpclib.Fault(1,"Method Unavailable : %s" % method)

  def __call__(self,req):
    return serviceRequest(req,self._dispatch)
