import vampire
import time

config = vampire.loadConfig(__req__,".vampire")
layouts = config.get("Handlers","layouts_root")
layout = vampire.importModule("basic",layouts,__req__)

class Template(layout.Template):

  no_cache = True

  def renderTemplate(self):

    cache = vampire.ModuleCache()

    def renderModule(node,label):
      info = cache.moduleInfo(label)
      node.path.content = info.file
      node.mtime.content = time.asctime(time.localtime(info.mtime))
      node.atime.content = time.asctime(time.localtime(info.atime))
      node.hits.content = str(info.direct)

    keys = cache.cachedModules()
    keys.sort()

    self.template.module.repeat(renderModule,keys)

handler_html = vampire.Instance(Template)
