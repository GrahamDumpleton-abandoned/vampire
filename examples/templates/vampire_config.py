import vampire

config = vampire.loadConfig(__req__,".vampire")
layouts = config.get("Handlers","layouts_root")
layout = vampire.importModule("basic",layouts,__req__)

class Template(layout.Template):

  no_cache = True

  def renderTemplate(self,file=".vampire",raw=None):

    config = vampire.loadConfig(self.req,file)

    # Render PythonOptions.

    options = self.req.get_options()

    def renderOption(node,key):
      node.key.content = key
      node.value.content = options[key]

    keys = options.keys()
    keys.sort()

    self.template.htaccess.item.repeat(renderOption,keys)

    # Render config file defaults.

    defaults = config.defaults()

    def renderDefault(node,key):
      node.key.content = key
      node.value.content = defaults[key]

    keys = defaults.keys()
    keys.sort()

    self.template.context.name.content = file
    self.template.context.item.repeat(renderDefault,keys)

    # Render config file sections.

    def renderConfig(node,key,section):
      node.key.content = key
      node.value.content = config.get(section,key,raw=raw)

    def renderSection(node,section):
      node.name.content = section
      keys = config.options(section)
      keys.sort()
      node.item.repeat(renderConfig,keys,section)

    sections = config.sections()
    sections.sort()

    self.template.section.repeat(renderSection,sections)

handler_html = vampire.Instance(Template)
