import vampire

config = vampire.loadConfig(__req__,".vampire")
layouts = config.get("DEFAULT","__layouts_root__")
layout = vampire.importModule("basic",layouts,__req__)

class Template(layout.Template):

  def renderTemplate(self):

    fullname = self.req.session["profile"]["fullname"]

    self.template.fullname.content = fullname

    layout.Template.renderTemplate(self)

handler_html = vampire.Instance(Template)
