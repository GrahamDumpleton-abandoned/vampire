# COPYRIGHT 2001-2005 DUMPLETON SOFTWARE CONSULTING PTY LIMITED

from mod_python import apache

import imp
import md5
import os
import time
import string
import types
import sys

try:
  from threading import Lock
except:
  class Lock:
    def acquire(self): pass
    def release(self): pass

if not hasattr(types,"BooleanType"):
  False = 0
  True = 1


# Cut down request object made available
# only during the importing of a handler.

class _Request:

  def __init__(self,req):
    # mod_python 2.7.X
    if hasattr(req,"get_dirs"):
      self.get_dirs = req.get_dirs

    # mod_python 3.X
    if hasattr(req,"hlist"):
      self.hlist = req.hlist
      self.document_root = req.document_root
      self.interpreter = req.interpreter
      self.log_error = req.log_error

    # mod_python common
    self.server = req.server
    self.get_options = req.get_options
    self.get_config = req.get_config
    self.filename = req.filename
    self.uri = req.uri


class _ModuleInfo:

  def __init__(self,name,label,file,mtime):
    self.name = name
    self.label = label
    self.file = file
    self.mtime = mtime
    self.module = None
    self.generation = 0
    self.children = []
    self.atime = 0
    self.direct = 0
    self.indirect = 0
    self.lock = Lock()

class _ModuleCache:

  _prefix = "_vampire_"

  def __init__(self):
    self._cache = {}
    self._lock1 = Lock()
    self._lock2 = Lock()
    self._generation = 0

  def cachedModules(self):
    self._lock1.acquire()
    try:
      return self._cache.keys()
    finally:
      self._lock1.release()

  def moduleInfo(self,label):
    self._lock1.acquire()
    try:
      return self._cache[label]
    finally:
      self._lock1.release()

  def unloadModule(self,label):
    self._lock1.acquire()
    try:
      if self._cache.has_key(label):
	if hasattr(self._cache[label],"__purge__"):
	  try:
	    self._cache[label].__purge__()
	  except:
	    pass
	del self._cache[label]
    finally:
      self._lock1.release()

  def purgeDefunct(self):
    self._lock1.acquire()
    try:
      for label in self._cache.keys():
	cache = self._cache[label]
	if not os.path.exists(cache.file):
	  if hasattr(self._cache[label],"__purge__"):
	    try:
	      self._cache[label].__purge__()
	    except:
	      pass
	  del self._cache[label]
    finally:
      self._lock1.release()

  def forceReload(self,name,path):
    self._lock1.acquire()
    try:
      try:
	fp = None
	path = os.path.normpath(path)
	file = os.path.join(path,name) + ".py"
	label = self._moduleLabel(file)
	if self._cache.has_key(label):
	  cache = self._cache[label]
	  cache.mtime = 0
      except:
	pass
      else:
	fp.close()
    finally:
      self._lock1.release()

  def importModule(self,name,path,req=None):
    log = False
    if req != None:
      if req.get_config().has_key("PythonDebug"):
        if req.get_config()["PythonDebug"] == "1":
          log = True
    path = os.path.normpath(path)
    file = os.path.join(path,name) + ".py"
    label = self._moduleLabel(file)
    cache = None
    try:
      cache,reload = self._retrieveModule(name,label,file)
      cache.lock.acquire()
      if reload:
	module = imp.new_module(label)
	module.__file__ = file
	if cache.module != None:
	  if hasattr(cache.module,"__clone__"):
	    try:
	      cache.module.__clone__(module)
	    except:
	      if hasattr(cache.module,"__purge__"):
		try:
		  cache.module.__purge__()
		except:
		  pass
	      if log:
		msg = "vampire: Purging module '%s'" % file
		apache.log_error(msg,apache.APLOG_NOERRNO|apache.APLOG_NOTICE)
	      cache.module = None
	      module = imp.new_module(label)
	      module.__file__ = file
	  if log:
	    if cache.module == None:
	      msg = "vampire: Importing module '%s'" % file
	      apache.log_error(msg,apache.APLOG_NOERRNO|apache.APLOG_NOTICE)
	    else:
	      msg = "vampire: Reimporting module '%s'" % file
	      apache.log_error(msg,apache.APLOG_NOERRNO|apache.APLOG_NOTICE)
        else:
	  if log:
	    msg = "vampire: Importing module '%s'" % file
	    apache.log_error(msg,apache.APLOG_NOERRNO|apache.APLOG_NOTICE)
	#if req != None:
	#  req = _Request(req)
	module.__req__ = req
	try:
	  execfile(file,module.__dict__)
	except:
	  if cache.module is None:
	    # Initial import. Discard cache entry.
	    del self._cache[label]
	  raise
	cache.module = module
	del module.__dict__["__req__"]
	self._lock2.acquire()
	self._generation = self._generation + 1
	cache.generation = self._generation
	self._lock2.release()
	cache.atime = time.time()
	cache.direct = 1
	cache.indirect = 0
	children = []
	for object in module.__dict__.values():
	  if type(object) == types.ModuleType:
	    if object.__name__[:len(self._prefix)] == self._prefix:
	      children.append(object.__name__)
	cache.children = children
      else:
	cache.direct = cache.direct + 1
	cache.atime = time.time()
	module = cache.module
      return module
    finally:
      if cache is not None:
        cache.lock.release()

  def _retrieveModule(self,name,label,file):
    self._lock1.acquire()
    try:

      # Check if this is a new module.
      if not self._cache.has_key(label):
	mtime = os.path.getmtime(file)
	cache = _ModuleInfo(name,label,file,mtime)
	self._cache[label] = cache
	return (cache,True)

      # Grab entry from cache.
      cache = self._cache[label]

      # Has modification time changed.
      try:
	mtime = os.path.getmtime(file)
      except:
	# Must have been removed just then.
	# We return currently cached module
	# and avoid a reload. Defunct module
	# would need to be purged later.
	return (cache,False)
      if mtime != cache.mtime:
	cache.mtime = mtime
	return (cache,True)

      # Check if children have changed or have
      # been reloaded since module last used.
      if cache.children != []:
	atime = time.time()
	dependencies = []
	visited = { label: 1 }
	dependencies.extend(cache.children)
	while len(dependencies) != 0:
	  next = dependencies.pop()
	  if not visited.has_key(next):
	    if self._cache.has_key(next):
	      temp = self._cache[next]
	      temp.indirect = temp.indirect + 1
	      temp.atime = atime

	      # Child has been reloaded.
	      if temp.generation > cache.generation:
		return (cache,True)

	      try:
		mtime = os.path.getmtime(temp.file)
		# Child has been modified.
		if mtime != temp.mtime:
		  return (cache,True)
	      except:
		# Module must have been removed. Don't
		# cause this to force a reload though as
		# can cause problems.
		pass

	      dependencies.extend(temp.children)
	    else:
	      return (cache,True)

	    visited[next] = 1

      return (cache,False)

    finally:
      self._lock1.release()

  def _moduleLabel(self,file):
    # The label is used in the __name__ field of
    # the module and then used in determining
    # child module imports. Thus needs to be
    # unique. We don't really want to use a
    # module name which is a filesystem path.
    # Hope MD5 hex digest is okay.
    stub = os.path.splitext(file)[0]
    label = md5.new(stub).hexdigest()
    label = self._prefix + label
    label = label + "_" + str(len(stub))
    return label


_moduleCache = _ModuleCache()

def ModuleCache():
  return _moduleCache

def importModule(name,path,req=None):
  return _moduleCache.importModule(name,path,req)
