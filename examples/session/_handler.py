from mod_python import apache

import vampire
import os

config = vampire.loadConfig(__req__,".vampire")

cheetah = vampire.importModule("_handler",
    config.get("DEFAULT","__cheetah_root__"),__req__)

psp = vampire.importModule("_handler",
    config.get("DEFAULT","__psp_root__"),__req__)

def handler_html(req):

  # This default handler for ".html" requests provides
  # support for both Cheetah templates and PSP.

  target = os.path.splitext(req.filename)[0]

  # First look to see if request can be handle by a
  # Cheetah template. Note that the ".tmpl" file must
  # have been compiled into an appropriate ".py" file.

  if os.path.exists(target+".tmpl"):
    return cheetah.handler_html(req)

  # Now look to see if it could instead be handled as
  # PSP request.

  if os.path.exists(target+".psp"):
    return psp.handler_html(req)

  # If still can't handle the request, pass the request
  # back to Apache so it can serve up any static ".html"
  # files.

  return apache.DECLINED
