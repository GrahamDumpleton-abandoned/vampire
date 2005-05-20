import vampire

def handler_html(req,message=""):
  if not message:
    message = "Give Blood!"

  template = vampire.loadTemplate(req.filename,"vampire:node")

  template.message.content = message

  req.content_type = "text/html"
  req.send_http_header()

  req.write(template.render())
