import vampire
import sys

config = vampire.loadConfig(__req__,".vampire")
layouts = config.get("Handlers","layouts_root")
layout = vampire.importModule("basic",layouts,__req__)

class Template(layout.Template):

  no_cache = True

  def renderTemplate(self):

    def renderModule(node,label):
      node.label.content = label
      if hasattr(sys.modules[label],"__file__"):
	node.path.content = sys.modules[label].__file__

    keys = sys.modules.keys()
    keys.sort()

    self.template.module.repeat(renderModule,keys)

handler_html = vampire.Instance(Template)
