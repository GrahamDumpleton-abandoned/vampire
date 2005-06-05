from mod_python import apache

import vampire
import os

config = vampire.loadConfig(__req__,".vampire")

cheetah = vampire.importModule("_handler",
    config.get("DEFAULT","__cheetah_root__"),__req__)

psp = vampire.importModule("_handler",
    config.get("DEFAULT","__psp_root__"),__req__)

def handler_html(req):

  target = os.path.splitext(req.filename)[0]

  if os.path.exists(target+".tmpl"):
    return cheetah.handler_html(req)

  if os.path.exists(target+".psp"):
    return psp.handler_html(req)

  return apache.DECLINED
