from mod_python import apache

import os
import vampire

# Default handler for HTML.

def handler_html(req):

  # Check for existance of PSP source file.

  path = os.path.splitext(req.filename)[0] + ".psp"

  if os.path.exists(path):

    # Hand off request to PSP handler.

    from mod_python import psp

    req.content_type = "text/html"

    config = vampire.loadConfig(req,".vampire")

    settings = {}

    for key,value in config.items("Settings"):
      settings[key] = value

    if hasattr(req,"form"):
      settings["form"] = req.form

    template = psp.PSP(req,filename=path,vars=settings)

    template.run()

    return apache.OK

  return apache.DECLINED

# Default handler for PSP.

def handler_psp(req):
  if os.path.exists(req.filename):
    return apache.HTTP_NOT_FOUND
  return apache.DECLINED
