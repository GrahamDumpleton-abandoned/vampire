from mod_python import apache

import os
import sys
import ConfigParser

import vampire

# Default handler.

def handler_html(req,file=".vampire",mode="fill"):

  # Load the page template.

  if not os.path.exists(req.filename):
    return apache.DECLINED

  template = vampire.loadTemplate(req.filename,"vampire:node")

  config = vampire.loadConfig(req,file)

  # Render PythonOptions.

  options = req.get_options()

  def renderOption(node,key):
    node.key.content = key
    node.value.content = options[key]

  keys = options.keys()
  keys.sort()

  template.htaccess.item.repeat(renderOption,keys)

  # Render config file defaults.

  defaults = config.defaults()

  def renderDefault(node,key):
    node.key.content = key
    node.value.content = defaults[key]

  keys = defaults.keys()
  keys.sort()

  template.context.name.content = file
  template.context.item.repeat(renderDefault,keys)

  # Render config file sections.

  def renderConfig(node,key,section):
    node.key.content = key
    if mode != "raw":
      node.value.content = config.get(section,key)
    else:
      node.value.content = config.get(section,key,raw=1)

  def renderSection(node,section):
    node.name.content = section
    keys = config.options(section)
    keys.sort()
    node.item.repeat(renderConfig,keys,section)

  sections = config.sections()
  sections.sort()

  template.section.repeat(renderSection,sections)

  # Return the rendered page content.

  req.content_type = "text/html"
  req.headers_out['Pragma'] = 'no-cache' 
  req.headers_out['Cache-Control'] = 'no-cache' 
  req.headers_out['Expires'] = '-1' 
  req.send_http_header()
  req.write(template.render())

  return apache.OK
