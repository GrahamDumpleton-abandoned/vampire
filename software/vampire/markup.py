# COPYRIGHT 2004-2005 DUMPLETON SOFTWARE CONSULTING PTY LIMITED

import os
import time

import HTMLTemplate

try:      
  from threading import Lock
except:   
  class Lock:
    def acquire(self): pass
    def release(self): pass

# Create version of template which splits cloning out from
# rendering so we can manage template caching. The callback
# is also eliminated.

class _Template(HTMLTemplate.Template):

    def __init__(self, html, attribute='node',
            codecs=(HTMLTemplate.defaultEncoder, HTMLTemplate.defaultDecoder)):
        HTMLTemplate.Template.__init__(self,None,html,attribute,codecs)

    def render(self):
        """Render this template; *args will be passed directly to the template.
        """
        collector = []
        self._renderContent(collector)
        try: # quick-n-dirty error reporting; not a real substitute for type-
            # checking for bad value assignments at point of origin, but cheap
            return ''.join(collector)
        except TypeError:
            raise TypeError, "Can't render template: some node's content " \
                    "was set to a non-text value."

# Template cache. Will automatically reload a file if it
# has changed. This includes its modification time being
# set backwards in time.

class _TemplateInfo:

  def __init__(self,path,mtime,template,attribute):
    self.path = path
    self.mtime = mtime
    self.template = template
    self.attribute = attribute
    self.atime = time.time()
    self.hits = 0

class _TemplateCache:

  def __init__(self):
    self._cache = {}
    self._lock = Lock()
    self._frozen = False

  def cachedTemplates(self):
    self._lock.acquire()
    try:
      return self._cache.keys()
    finally:
      self._lock.release()

  def templateInfo(self,path):
    self._lock.acquire()
    try:
      path = os.path.normpath(path)
      return self._cache[path]
    finally:
      self._lock.release()

  def unloadTemplate(self,path):
    self._lock.acquire()
    try:
      path = os.path.normpath(path)
      if self._cache.has_key(path):
        del self._cache[path]
    finally:
      self._lock.release()

  def freezeCache(self):
    self._frozen = True

  def loadTemplate(self,path,attribute="node"):
    self._lock.acquire()
    try:
      record = None
      # ensure the path is normalised
      path = os.path.normpath(path)
      # is page template already loaded
      if self._cache.has_key(path):
        record = self._cache[path]
        # check if reloads have been disabled
        if not self._frozen:
          # has page template been changed
          try:
            mtime = os.path.getmtime(path)
          except:
            # page template must not exist
            del self._cache[path]
            raise
          else:
            if record.mtime != mtime:
              # force reloading of page template
              del self._cache[path]
              record = None
            elif record.attribute != attribute:
              # name of attribute has changed
              del self._cache[path]
              record = None
      # need to load the page template
      if record is None:
        file = open(path,"r")
        content = file.read()
        mtime = os.path.getmtime(path)
        template = _Template(content,attribute)
        record = _TemplateInfo(path,mtime,template,attribute)
        file.close()
        self._cache[path] = record
      else:
        template = record.template
      # return clone of page template
      record.hits = record.hits + 1
      record.atime = time.time()
      return template._initRichClone(HTMLTemplate.CloneNode(template))
    finally:
      self._lock.release()


_templateCache = _TemplateCache()

def TemplateCache():
  return _templateCache

def loadTemplate(path,attribute="node"):
  return _templateCache.loadTemplate(path,attribute)
