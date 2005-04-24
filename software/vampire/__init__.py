# COPYRIGHT 2004-2005 DUMPLETON SOFTWARE CONSULTING PTY LIMITED

__version__ = "1.7"

from mod_python import apache

from lookup import _handler, _publisher, _select, _form, _authenticate_basic
from lookup import Handler, Publisher, PathInfo, PathArgs

handler = _handler
publisher = _publisher
processForm = _form
loginhandler = _authenticate_basic

# Setup redirections for all handlers except for
# the PythonHandler directive. Some are actually
# redudant and don't do anything. Need them here
# though to get around "PythonHandlerModule" bug.

def connectionhandler(conn):
  return apache.OK

def postreadrequesthandler(req):
  # return _select(req,"postreadrequesthandler")
  return apache.OK

def transhandler(req):
  # return _select(req,"transhandler")
  return apache.OK

def headerparserhandler(req):
  # return _select(req,"headerparserhandler")
  return apache.OK

def inithandler(req):
  # return _select(req,"inithandler")
  return apache.OK

def accesshandler(req):
  return _select(req,"accesshandler")

def authenhandler(req):
  return _select(req,"authenhandler")

def authzhandler(req):
  return _select(req,"authzhandler")

def typehandler(req):
  return _select(req,"typehandler")

def fixuphandler(req):
  return _select(req,"fixuphandler")

def loghandler(req):
  return _select(req,"loghandler")

def cleanuphandler(req):
  return _select(req,"cleanuphandler")

# Shortcuts for the module cache and the
# configuration cache.

from cache import ModuleCache, importModule
from config import ConfigCache, loadConfig

# Shortcut for the template cache. Import this
# inside of a try block as it will fail if the
# HTMLTemplate module hasn't been installed.

try:
  from markup import TemplateCache, loadTemplate
except:
  pass

# Shortcut for XML-RPC request handler. Import
# this inside a try block as it may fail if
# OpenBSD is being used and Apache isn't linked
# with multithreading but Python was built with
# multithreading enabled.

try:
  from xmlrpc import serviceRequest, Service
except:
  pass
