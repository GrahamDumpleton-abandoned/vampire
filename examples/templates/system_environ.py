import vampire
import os

config = vampire.loadConfig(__req__,".vampire")
layouts = config.get("Handlers","layouts_root")
layout = vampire.importModule("basic",layouts,__req__)

class Template(layout.Template):

  no_cache = True

  def renderTemplate(self):

    def renderItem(node,name):
      node.name.content = name
      node.value.content = os.environ[name]

    names = list(os.environ.keys())
    names.sort()

    self.template.item.repeat(renderItem,names)

handler_html = vampire.Instance(Template)
