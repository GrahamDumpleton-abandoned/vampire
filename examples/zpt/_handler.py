from mod_python import apache

import os
import vampire

from ZopePageTemplates import PageTemplate

# Default handler for HTML.

def handler_html(req,**kwargs):

  # Check for existance of ZPT source file.

  path = os.path.splitext(req.filename)[0] + ".zpt"

  if os.path.exists(path):

    layout_file = os.path.join(os.path.dirname(__file__),"_layout.zpt")

    layout = PageTemplate()
    layout.write(open(layout_file,"r").read())

    config = vampire.loadConfig(req,".vampire")

    settings = {}

    for key,value in config.items("Settings"):
      settings[key] = value

    settings["request"] = req
    settings["form"] = kwargs

    page = PageTemplate()
    page.write(open(path,"r").read())

    settings["here"] = { "layout": layout }

    content = page.pt_render(extra_context=settings)

    req.content_type = page.content_type
    req.send_http_header()

    req.write(content)

    return apache.OK

  return apache.DECLINED

# Default handler for ZPT.

def handler_zpt(req):
  if os.path.exists(req.filename):
    return apache.HTTP_NOT_FOUND
  return apache.DECLINED
