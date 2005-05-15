import vampire

config = vampire.loadConfig(__req__,".vampire")
layouts = config.get("Handlers","layouts_root")
layout = vampire.importModule("basic",layouts,__req__)

class Template(layout.Template):

  no_cache = True

  def renderTemplate(self,**fields):

    def renderItem(node,name):
      node.name.content = name
      node.value.content = str(fields[name])

    names = list(fields.keys())
    names.sort()

    self.template.item.repeat(renderItem,names)

handler_html = vampire.Instance(Template)
