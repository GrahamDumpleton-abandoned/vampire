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

  def renderItem(node,name):
    node.name.content = name
    node.value.content = os.environ[name]

  names = list(os.environ.keys())
  names.sort()

  template.item.repeat(renderItem,names)

  # Return the rendered page content.

  req.content_type = "text/html"
  req.headers_out['Pragma'] = 'no-cache' 
  req.headers_out['Cache-Control'] = 'no-cache' 
  req.headers_out['Expires'] = '-1' 
  req.send_http_header()
  req.write(template.render())

  return apache.OK
