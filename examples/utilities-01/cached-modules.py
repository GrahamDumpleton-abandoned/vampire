from mod_python import apache

import os
import sys
import time

import vampire

# Handler for ".html" request.

def handler_html(req):

  # Load the page template.

  if not os.path.exists(req.filename):
    return apache.DECLINED

  template = vampire.loadTemplate(req.filename,"vampire:node")

  # Fill in the page content.

  cache = vampire.ModuleCache()

  def renderModule(node,label):
    info = cache.moduleInfo(label)
    node.path.content = info.file
    node.mtime.content = time.asctime(time.localtime(info.mtime))
    node.atime.content = time.asctime(time.localtime(info.atime))
    node.hits.content = str(info.direct)

  keys = cache.cachedModules()
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
