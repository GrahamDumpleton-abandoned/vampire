# COPYRIGHT 2001-2005 DUMPLETON SOFTWARE CONSULTING PTY LIMITED

from mod_python import apache

import imp
import md5
import os
import time
import string
import types
import sys

import config 

_configCache = config.ConfigCache()


try:
  from threading import Lock
except:
  class Lock:
    def acquire(self): pass
    def release(self): pass

if not hasattr(types,"BooleanType"):
  False = 0
  True = 1


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
    self._frozen = False

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

  def freezeCache(self):
    self._frozen = True

  def importModule(self,name,path,req=None):
    # Raise an exception so as to determine the stack
    # frame of the parent frame which has requested the
    # module be imported. We need to skip any frames
    # which refer to this module, something which can
    # occur when "import" statement is being used.

    try:
      raise Exception
    except:
      parent = sys.exc_info()[2].tb_frame.f_back
      while parent.f_globals.has_key("__file__") and \
          parent.f_globals["__file__"] == __file__:
        parent = parent.f_back

    # Allow shortcut whereby if path is not set that we
    # use the directory that the parent module doing the
    # import is located in.

    if path is None:
      path = os.path.dirname(parent.f_code.co_filename)

    # Where request object isn't explicitly provided,
    # see if copy which is stashed in module while it is
    # being imported exists and use that.

    if req is None:
      req = parent.f_globals.get("__req__",None)

    # Ascertain if debugging is enabled and thus whether
    # module imports and reimports etc should be logged.

    log = False
    if req != None:
      if req.get_config().has_key("PythonDebug"):
        if req.get_config()["PythonDebug"] == "1":
          log = True

    # Calculate the potential name of the target module
    # file and determine the coded module name which
    # would be used to identify it.

    path = os.path.normpath(path)

    target = os.path.join(path,name)

    file = None

    if os.path.isdir(target):
      # XXX Haven't been able to work out yet how to
      # support packages. Importing the top level of the
      # package works okay, but importing a sub module
      # of the package directly, where it isn't
      # automatically imported by the top level of the
      # package doesn't work. This is because the code
      # inside Python appears to use context information
      # derived from sys.modules to work out the parent
      # module, but Vampire does not store anything in
      # sys.modules.

      raise ImportError("Vampire does not support packages.")

      #target = os.path.join(target,"__init__.py")
      #if os.path.exists(target):
      #  file = target

    if not file:
      file = os.path.join(path,name) + ".py"

    label = self._moduleLabel(file)

    # See if requested module has already been imported
    # previously within the context of this request. If
    # it has we skip any dependency checks to ensure the
    # same actual module instance is used.

    if req and hasattr(req,"vampire"):
        if req.vampire.has_key("modules"):
          if req.vampire["modules"].has_key(label):
            return req.vampire["modules"][label]

    # Now move on to trying to find the actual module.

    try:
      cache = None

      # First determine if the module has been loaded
      # previously. If not already loaded or if a
      # dependency of the module has been changed on
      # disk or reloaded since parent was loaded, must
      # load the module.

      cache,load = self._retrieveModule(name,label,file)

      # Make sure that the cache entry is locked by the
      # thread so that other threads in a multithreaded
      # system don't try and load the same module at the
      # same time.

      cache.lock.acquire()

      if load:

	# Setup a new empty module to load the code for
        # the module into.

        module = imp.new_module(label)
        module.__file__ = file

	# If the module was previously loaded we need to
	# manage the transition to the new instance of
	# the module that is being loaded to replace it.
        # This entails calling the special clone method,
        # if provided, in the existing module. Using this
	# method the existing method can selectively
	# indicate what should be transfered over to the
	# next instance of the module including thread
	# locks. If this process fails the special purge
	# method is called if provided to indicate that
	# the existing module is being forcibly purged
        # out of the system. In that case any existing
        # state will not be transferred.

        if cache.module != None:
          if hasattr(cache.module,"__clone__"):
            try:
              # Copy existing state data from existing
              # module instance to new module instance.

              if log:
                msg = "vampire: Cloning module '%s'" % file
                apache.log_error(msg,apache.APLOG_NOERRNO|apache.APLOG_NOTICE)

              cache.module.__clone__(module)
            except:
              # Forcibly purging module from system.

              if hasattr(cache.module,"__purge__"):
                try:
                  cache.module.__purge__()
                except:
                  pass

              if log:
                msg = "vampire: Purging module '%s'" % file
                apache.log_error(msg,apache.APLOG_NOERRNO|apache.APLOG_NOTICE)

              # Setup a fresh new module yet again.

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

	# Save the request object into the global data
	# of the module, but only for the lifetime of
	# the actual module importing process.

        module.__req__ = req

	# Create a temporary place where information
	# about child imports performed by the module
	# can be put.

        module.__children__ = []

        # Place a reference to the module within the
        # request specific cache of imported modules.
	# This makes module lookup more efficient when
	# the same module is imported more than once
	# within the context of a request. In the case
        # of a cyclical import, avoids a never ending
        # recursive loop.

        if req:
          if not hasattr(req,"vampire"):
            req.vampire = {}

          if not req.vampire.has_key("modules"):
            req.vampire["modules"] = {}

          req.vampire["modules"][label] = module

        # Perform the actual import of the module.

        try:
          execfile(file,module.__dict__)

        except:
	  # Importation of module has failed for some
	  # reason. If this is the very first import of
	  # the module, need to discard the cache entry
	  # entirely else a subsequent attempt to load
	  # the module will wrongly think it was
	  # successfully loaded already.

          if cache.module is None:
            del self._cache[label]

          raise

	# If this is a child import of some parent
	# module, add this module as a child of the
	# parent.

        globals = parent.f_globals

        if globals.has_key("__children__"):
            globals["__children__"].append(label)

        # Remove the request object from the globals
        # of the module.

        del module.__dict__["__req__"]

        # Replace the existing module with the new one.

        cache.module = module

	# Increment the generation count of the global
	# state of all modules. This is used in the
	# dependency management scheme for reloading to
	# determine if a module dependency has been
	# reloaded since it was loaded.

        self._lock2.acquire()
        self._generation = self._generation + 1
        cache.generation = self._generation
        self._lock2.release()

        # Update access time and reset access counts.

        cache.atime = time.time()
        cache.direct = 1
        cache.indirect = 0

        # Determine modules that this module depends
        # on. That is, the list of modules the module
        # imported within global scope.

        cache.children = module.__children__

        del module.__dict__["__children__"]

      else:
	# Didn't need to reload the module so simply
	# increment access counts and last access time.

        cache.direct = cache.direct + 1
        cache.atime = time.time()

        # Place a reference to the module within the
        # request specific cache of imported modules.
	# This makes module lookup more efficient when
	# the same module is imported more than once
	# within the context of a request.

        module = cache.module

        if req:
          if not hasattr(req,"vampire"):
            req.vampire = {}

          if not req.vampire.has_key("modules"):
            req.vampire["modules"] = {}

          req.vampire["modules"][label] = module

      return module

    finally:
      # Lock on cache object can now be released.

      if cache is not None:
        cache.lock.release()

  def _retrieveModule(self,name,label,file):
    try:
      self._lock1.acquire()

      # Check if this is a new module.

      if not self._cache.has_key(label):
        mtime = os.path.getmtime(file)
        cache = _ModuleInfo(name,label,file,mtime)
        self._cache[label] = cache
        return (cache,True)

      # Grab entry from cache.

      cache = self._cache[label]

      # Check if reloads have been disabled.

      if self._frozen:
        return (cache,False)

      # Has modification time changed.

      try:
        mtime = os.path.getmtime(file)
      except:
	# Must have been removed just then. We return
	# currently cached module and avoid a reload.
	# Defunct module would need to be purged later.

        return (cache,False)
      if mtime != cache.mtime:
        cache.mtime = mtime
        return (cache,True)

      # Check if children have changed or have been
      # reloaded since module last used.

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
    # The label is used in the __name__ field of the
    # module and then used in determining child module
    # imports. Thus really needs to be unique. We don't
    # really want to use a module name which is a
    # filesystem path. Hope MD5 hex digest is okay.

    stub = os.path.splitext(file)[0]
    label = md5.new(stub).hexdigest()
    label = self._prefix + label
    label = label + "_" + str(len(stub))
    return label


_moduleCache = _ModuleCache()

def ModuleCache():
  return _moduleCache

importModule = _moduleCache.importModule


class ModuleLoader:

  def __init__(self,directory,req):
    self.__directory = directory
    self.__req = req

  def load_module(self,fullname):
    apache.log_error("load %s"%fullname)
    return importModule(fullname,self.__directory,self.__req)

class ModuleImporter:

  def find_module(self,fullname,path=None):
    apache.log_error("find %s %s" %(fullname,path))

    # Raise an exception so as to determine the stack
    # frame of the parent frame which has requested the
    # module be imported.

    try:
      raise Exception
    except:
      parent = sys.exc_info()[2].tb_frame.f_back

    # Only consider using import caching mechanism if
    # request object is present as "__req__", filename
    # is defined by "__file__" and use of import hooks
    # has been enabled.

    globals = parent.f_globals

    if not globals.has_key("__req__"):
      return None

    if not globals.has_key("__file__"):
      return None

    options = {}

    req = globals["__req__"]

    if req is None:
      return None

    options = req.get_options()

    if not options.has_key("VampireImportHooks"):
      return None

    if options["VampireImportHooks"] not in ["On","on"]:
      return None

    # Check directory in which parent is located.

    file = None
    ispkg = False

    directory = os.path.dirname(globals["__file__"])

    target = os.path.join(directory,fullname)
    if os.path.isdir(target):
      target = os.path.join(target,"__init__.py")
      if os.path.exists(target):
        file = target
        ispkg = True

    if not file:
      target = os.path.join(directory,fullname) + ".py"
      if os.path.exists(target):
        file = target

    # If not in the parents own directory, check
    # along the Vampire module search path.

    def _search(name,path,req):
      for directory in path:
        target = os.path.join(directory,name) + ".py"
        if os.path.exists(target):
          return target

    if not file:
      name = ".vampire"
      if options.has_key("VampireHandlersConfig"):
        name = options["VampireHandlersConfig"]
      config = _configCache.loadConfig(req,name)
      section = "Modules"
      if options.has_key("VampireModulesSection"):
        section = options["VampireModulesSection"]
      path = None
      if config.has_option(section,"path"):
        path = config.get(section,"path").split(':')
      if path:
        file = _search(fullname,path,req)

    if not file:
      return None

    if ispkg:
      directory = os.path.dirname(os.path.dirname(file))
    else:
      directory = os.path.dirname(file)

    return ModuleLoader(directory,req)


sys.meta_path.insert(0,ModuleImporter())
