import vampire
import time

config = vampire.loadConfig(__req__,".vampire")
layouts = config.get("Handlers","layouts_root")
layout = vampire.importModule("basic",layouts,__req__)

class Template(layout.Template):

  no_cache = True
  
  def renderTemplate(self):                                                     

    cache = vampire.TemplateCache()

    def renderModule(node,path):
      node.path.content = path
      info = cache.templateInfo(path)
      node.node.content = info.attribute
      node.mtime.content = time.asctime(time.localtime(info.mtime))
      node.atime.content = time.asctime(time.localtime(info.atime))
      node.hits.content = str(info.hits)

    keys = cache.cachedTemplates()
    keys.sort()

    self.template.module.repeat(renderModule,keys)


handler_html = vampire.Instance(Template)
