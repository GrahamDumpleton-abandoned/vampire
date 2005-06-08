from mod_python import apache

import os

psp = apache.import_module("mod_python.psp")

def handler_html(req,message=""):
  if not message:
    message = "Give Blood!"

  path = os.path.splitext(req.filename)[0] + ".psp"

  req.content_type = "text/html"
  req.send_http_header()

  settings = { "message": message }
  template = psp.PSP(req,filename=path,vars=settings)
  template.run()
