from mod_python import apache

import os
import sys

import vampire

def handler_html(req):

  # Load the page template.

  if not os.path.exists(req.filename):
    return apache.DECLINED

  template = vampire.loadTemplate(req.filename,"vampire:node")

  # Render request object data.

  details = {}

  details["the_request"] = req.the_request
  details["method"] = req.method
  details["unparsed_uri"] = req.unparsed_uri
  details["uri"] = req.uri
  details["path_info"] = req.path_info
  details["args"] = req.args or ""
  details["protocol"] = req.protocol
  details["proto_num"] = str(req.proto_num)
  details["hostname"] = req.hostname
  details["interpreter"] = req.interpreter
  details["user"] = req.user or ""

  def renderObject(node,key):
    node.key.content = key
    node.value.content = details[key]

  keys = details.keys()
  keys.sort()

  template.object.item.repeat(renderObject,keys)

  # Render request headers.

  headers = req.headers_in

  def renderHeader(node,key):
    node.key.content = key
    node.value.content = headers[key]

  keys = headers.keys()
  keys.sort()

  template.headers.item.repeat(renderHeader,keys)

  # Return the rendered page content.

  req.content_type = "text/html"
  req.headers_out['Pragma'] = 'no-cache' 
  req.headers_out['Cache-Control'] = 'no-cache' 
  req.headers_out['Expires'] = '-1' 
  req.send_http_header()
  req.write(template.render())

  return apache.OK
