from mod_python import apache

import os
import vampire

__psp_root__ = os.path.join(os.path.dirname(__file__),"..","psp")
psp = vampire.importModule("_handler",__psp_root__,__req__)

class Handler(psp.Servlet):

  def __call__(self,message=""):
    if not message:
      message = "Give Blood!"

    self.vars["message"] = message

    self.render()

handler_html = vampire.Instance(Handler)
