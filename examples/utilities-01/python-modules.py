from mod_python import apache

import os
import sys

import vampire

# Handler for ".html" request.

def handler_html(req):

  # Load the page template.

  if not os.path.exists(req.filename):
    return apache.DECLINED

  template = vampire.loadTemplate(req.filename,"vampire:node")

  # Fill in the page content.

  def renderModule(node,label):
    node.label.content = label
    if hasattr(sys.modules[label],"__file__"):
      node.path.content = sys.modules[label].__file__

  keys = sys.modules.keys()
  keys.sort()

  template.module.repeat(renderModule,keys)

  # Return the rendered page content.

  req.content_type = "text/html"
  req.headers_out['Pragma'] = 'no-cache' 
  req.headers_out['Cache-Control'] = 'no-cache' 
  req.headers_out['Expires'] = '-1' 
  req.send_http_header()
  req.write(template.render())

  return apache.OK
