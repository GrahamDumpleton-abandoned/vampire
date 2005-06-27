from mod_python import apache
from mod_python import util
import os

def handler_html(req):
  directory = os.path.dirname(__file__)
  file = "../../../articles/modpython-001.html"
  target = os.path.join(directory,file)

  target = os.path.normpath(target)

  if not os.path.exists(target):
    return apache.DECLINED

  util.redirect(req,file)
