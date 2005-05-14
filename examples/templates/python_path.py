import vampire
import sys

config = vampire.loadConfig(__req__,".vampire")
layouts = config.get("Handlers","layouts_root")
layout = vampire.importModule("basic",layouts,__req__)

class Template(layout.Template):

  no_cache = True

  def renderTemplate(self):

    def renderDirectory(node,path):
      node.path.content = path

    self.template.directory.repeat(renderDirectory,sys.path)

handler_html = vampire.Instance(Template)
