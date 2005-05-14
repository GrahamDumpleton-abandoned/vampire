# COPYRIGHT 2004-2005 DUMPLETON SOFTWARE CONSULTING PTY LIMITED

import os
import sys
import string
import posixpath
import ConfigParser

try:
  from threading import Lock
except:
  class Lock:
    def acquire(self): pass
    def release(self): pass

def _ConfigParser(*params):
  config = ConfigParser.ConfigParser(*params)
  config.optionxform = str
  return config

class _Config:

  def __init__(self,config,defaults,req):
    self._config = config
    self._defaults = defaults
    self._options = req.get_options()

  def __getattr__(self,name):
    return getattr(self._config,name)

  def get(self,section,option,raw=0,vars=None):
    temp = {}
    temp.update(self._config.defaults())
    temp.update(self._options)
    if vars: temp.update(vars)
    temp.update(self._defaults)
    return self._config.get(section,option,raw=raw,vars=temp)

  if hasattr(ConfigParser.ConfigParser,"items"):

    # Note that items() in ConfigParser actually
    # stuffs everything in one dictionary in
    # order to make this work. Thus key/values
    # which are a source of interpolation and
    # not actually defined in the section itself
    # are also returned. This is not very nice.

    def items(self,section,raw=0,vars=None):
      temp = {}
      temp.update(self._config.defaults())
      temp.update(self._options)
      if vars: temp.update(vars)
      temp.update(self._defaults)
      return self._config.items(section,raw=raw,vars=temp)

  def defaults(self):
    temp = {}
    temp.update(self._config.defaults())
    temp.update(self._defaults)
    return temp

class _ConfigEntry:

  def __init__(self,config,file,mtime):
    self.config = config
    self.file = file
    self.mtime = mtime

class _ConfigCache:

  def __init__(self):
    self._cache = {}
    self._lock = Lock()

  def _search(self,req,name):

    result = {
      "__handler_root__" : "",
      "__config_root__" : "",
      "__config_file__" : "",
      "__config_mtime__" : "",
      "__baseurl_abs__" : "",
      "__baseurl_rel__" : ""
    }

    # Try a couple of different ways of determining
    # the root where the PythonHandler directive was
    # specified.

    handler_root = None

    if hasattr(req,"hlist"):
      # In mod_python 3.X have the req.hlist member.
      handler_root = req.hlist.directory

    elif hasattr(req,"get_dirs"):
      # In mod_python 2.X have the req.get_dirs() method.
      handler_root = req.get_dirs()["PythonHandler"]

    # Couldn't determine upper bounds of search.

    if handler_root is None:
      return result

    # Workaround bug in mod_python where it doesn't take
    # into consideration that Apache passes paths to it
    # in POSIX pathname format and thus it goes and adds
    # an extra trailing '\' on Win32 platforms.

    if handler_root[-1] == '\\':
      handler_root = handler_root[:-1]

    # Also want to drop the trailing '/' that will be put
    # on the path by mod_python anyway. Assumed that the
    # handler root can never be just '/' to start with.

    if handler_root[-1] == '/':
      handler_root = handler_root[:-1]

    handler_root = posixpath.normpath(handler_root)

    # Now search back up directories for file.

    result["__handler_root__"] = handler_root

    config_file = ""

    # Need to check for special case where request is
    # against a directory. This will only occur where
    # config is being requested in phase prior to that
    # corresponding to the PythonHandler directive.

    if os.path.isdir(req.filename):
      config_root = req.filename
    else:
      config_root = posixpath.dirname(req.filename)

    baseurl_abs = posixpath.dirname(req.uri)
    baseurl_rel = "."

    config_root_prev = config_root
    baseurl_abs_prev = baseurl_abs
    baseurl_rel_prev = baseurl_rel

    while len(config_root) >= len(handler_root):

      config_file = posixpath.join(config_root,name)

      if os.path.exists(config_file):
        config_root = posixpath.normpath(config_root)
        baseurl_abs = posixpath.normpath(baseurl_abs)
        baseurl_rel = posixpath.normpath(baseurl_rel)

	result["__config_root__"] = config_root
	result["__config_file__"] = config_file
	result["__baseurl_abs__"] = baseurl_abs
	result["__baseurl_rel__"] = baseurl_rel

	result["__config_mtime__"] = "0"

        return result

      config_root_prev = config_root
      baseurl_abs_prev = baseurl_abs
      baseurl_rel_prev = baseurl_rel

      config_root = posixpath.split(config_root)[0]
      baseurl_abs = posixpath.split(baseurl_abs)[0]
      baseurl_rel = posixpath.join(baseurl_rel,"..")

    baseurl_abs_prev = posixpath.normpath(baseurl_abs_prev)
    baseurl_rel_prev = posixpath.normpath(baseurl_rel_prev)

    result["__config_root__"] = config_root_prev
    result["__config_file__"] = config_file
    result["__baseurl_abs__"] = baseurl_abs_prev
    result["__baseurl_rel__"] = baseurl_rel_prev

    return result

  def loadConfig(self,req,name=None):
    self._lock.acquire()
    try:
      # Fallback to default name if not specified.

      if not name:
	name = ".vampire"
	options = req.get_options()
	if options.has_key("VampireConfigDatabase"):
	  name = options["VampireConfigDatabase"]

      # Check to see if config has been cached
      # in the request object from a previous
      # lookup for this specific request object
      # or prepare cache as necessary. This speeds
      # subsequent searches in same request but
      # also ensures that same config object is
      # used in all cases within context of the
      # same request.

      if not hasattr(req,"vampire"):
        req.vampire = { "config": {} }
      elif not req.vampire.has_key("config"):
        req.vampire["config"] = {}
      elif req.vampire["config"].has_key(name):
        return req.vampire["config"][name]

      # Perform search back up directory hierarchy.

      defaults = self._search(req,name)

      # Empty, use cache or reload as necessary.

      if defaults["__handler_root__"] == "":
	config = _ConfigParser()
	entry = _Config(config,defaults,req)
      elif defaults["__config_mtime__"] == "":
        file = defaults["__config_file__"]
	if self._cache.has_key(file):
	  del self._cache[file]
	config = _ConfigParser()
	defaults["__config_file__"] = ""
	entry = _Config(config,defaults,req)
      else:
        file = defaults["__config_file__"]
	if not self._cache.has_key(file):
	  mtime = os.path.getmtime(file)
	  config = _ConfigParser()
	  config.read(file)
	  cache = _ConfigEntry(config,file,mtime)
	  self._cache[file] = cache
	  defaults["__config_mtime__"] = str(mtime)
	  entry = _Config(config,defaults,req)
	else:
	  cache = self._cache[file]
	  config = cache.config
	  mtime = os.path.getmtime(file)
	  if mtime != cache.mtime:
	    del self._cache[file]
	    config = _ConfigParser()
	    config.read(file)
	    cache = _ConfigEntry(config,file,mtime)
	    self._cache[file] = cache
	  defaults["__config_mtime__"] = str(mtime)
	  entry = _Config(config,defaults,req)
      req.vampire["config"][name] = entry
      return entry
    finally:
      self._lock.release()

  def purgeDefunct(self):
    self._lock.acquire()
    try:
      for file in self._cache.keys():
	if not os.path.exists(file):
	  del self._cache[file]
    finally:
      self._lock.release()


_configCache = _ConfigCache()

def ConfigCache():
  return _configCache

def loadConfig(req,name):
  return _configCache.loadConfig(req,name)
