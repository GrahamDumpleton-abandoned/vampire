from mod_python import apache

import os
import vampire

def handler_html(req):

  directory,name = os.path.split(os.path.splitext(req.filename)[0])

  module = vampire.importModule(name,directory)

  if not hasattr(module,"Servlet"):
    return apache.HTTP_NOT_FOUND

  _servlet = module.Servlet()

  _servlet.req = req

  try:
    _servlet.auth()
    _servlet.prep()
    if not _servlet.respond():
      return apache.HTTP_NO_CONTENT
    _servlet.wrapup()

  finally:
    _servlet._finally()

  return apache.OK
