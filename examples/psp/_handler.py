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

    template = psp.PSP(req,filename=path,vars=config.defaults())
    template.run()

    return apache.OK

  return apache.DECLINED

# Default handler for PSP.

def handler_psp(req):
  if os.path.exists(req.filename):
    return apache.HTTP_FORBIDDEN
  return apache.DECLINED
