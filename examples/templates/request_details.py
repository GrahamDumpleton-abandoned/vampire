import vampire

config = vampire.loadConfig(__req__,".vampire")
layouts = config.get("Handlers","layouts_root")
layout = vampire.importModule("basic",layouts,__req__)

class Template(layout.Template):

  no_cache = True

  def renderTemplate(self):

    details = {}

    details["the_request"] = self.req.the_request
    details["method"] = self.req.method
    details["unparsed_uri"] = self.req.unparsed_uri
    details["uri"] = self.req.uri
    details["path_info"] = self.req.path_info
    details["args"] = self.req.args or ""
    details["protocol"] = self.req.protocol
    details["proto_num"] = str(self.req.proto_num)
    details["hostname"] = self.req.hostname
    details["interpreter"] = self.req.interpreter
    details["user"] = self.req.user or ""

    def renderObject(node,key):
      node.key.content = key
      node.value.content = details[key]

    keys = details.keys()
    keys.sort()

    self.template.object.item.repeat(renderObject,keys)

    headers = self.req.headers_in

    def renderHeader(node,key):
      node.key.content = key
      node.value.content = headers[key]

    keys = headers.keys()
    keys.sort()

    self.template.headers.item.repeat(renderHeader,keys)

handler_html = vampire.Instance(Template)
