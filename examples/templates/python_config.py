import vampire

config = vampire.loadConfig(__req__,".vampire")
layouts = config.get("Handlers","layouts_root")
layout = vampire.importModule("basic",layouts,__req__)

class Template(layout.Template):

  no_cache = True

  def renderTemplate(self):

    config = self.req.get_config()

    def renderItem(node,key):
      node.key.content = key
      node.value.content = config[key]

    keys = list(config.keys())
    keys.sort()

    self.template.item.repeat(renderItem,keys)

handler_html = vampire.Instance(Template)
