from mod_python import apache

import vampire
import cgi
import os

def _search(req,settings,file):

  # Searches for file type associated with request by
  # first looking for file as extension of actual file
  # and then back up the directory hierarchy until the
  # document root is reached.

  target = os.path.splitext(req.filename)[0] + file
  if os.path.exists(target):
    return target

  document_root = settings["document_root"]

  directory = os.path.dirname(req.filename)
  while len(directory) >= len(document_root):
    target = os.path.join(directory,file)
    if os.path.exists(target):
      return target
    directory = os.path.split(directory)[0]

  return None


def _hnav(links,settings):

  output = []

  output.append('<ul>')

  for label,target in links:
    if target.find('%(') != -1:
      target = target % settings
    target = cgi.escape(target)
    label = cgi.escape(label)

    output.append('<li><a href="%s">%s</a>' % (target,label))
    output.append('<span class="divider"> : </span>')

  output.append('</ul>')

  return "".join(output)


def _links(groups,settings):

  output = []

  for name,links in groups:
    output.append('<h3>')
    output.append(cgi.escape(name))
    output.append('</h3>\n')

    output.append('<ul>')

    for label,target in links:
      if target.find('%(') != -1:
	target = target % settings
      target = cgi.escape(target)
      label = cgi.escape(label)

      output.append('<li><a href="%s">%s</a>' % (target,label))

    output.append('</ul>\n')

  return "".join(output)


def layout_html(req,template,**options):

  # Load in configuration settings for this
  # request. These will be used later on.

  config = vampire.loadConfig(req,".vampire")

  settings = {}

  for key,value in config.items("Settings"):
    settings[key] = value

  # Setup masthead.

  masthead = ""

  if options.has_key("masthead"):
    masthead = options["masthead"]
  else:
    module = None

    target = _search(req,settings,"_masthead.py")

    if target:
      directory = os.path.dirname(target)
      name = os.path.splitext(os.path.basename(target))[0]
      module = vampire.importModule(name,directory,req)

    if module:
      masthead = module.masthead(req)

  if masthead:
    template.masthead.content = masthead

  # Setup navigation links.

  navbar = []

  if options.has_key("navbar"):
    navbar = options["navbar"]

  else:
    module = None

    target = _search(req,settings,"_navbar.py")

    if target:
      directory = os.path.dirname(target)
      name = os.path.splitext(os.path.basename(target))[0]
      module = vampire.importModule(name,directory,req)

    if module:
      navbar = module.navbar(req)

  if navbar:
    template.hnav.raw = _hnav(navbar,settings)

  links = []

  if options.has_key("links"):
    links = options["links"]

  else:
    module = None

    target = _search(req,settings,"_links.py")

    if target:
      directory = os.path.dirname(target)
      name = os.path.splitext(os.path.basename(target))[0]
      module = vampire.importModule(name,directory,req)

    if module:
      links = module.links(req)

  if links:
    template.vnav.raw = _links(links,settings)

  # Setup footer.

  footer = ""

  if options.has_key("footer"):
    footer = options["footer"]
  else:
    module = None

    target = _search(req,settings,"_footer.py")

    if target:
      directory = os.path.dirname(target)
      name = os.path.splitext(os.path.basename(target))[0]
      module = vampire.importModule(name,directory,req)

    if module:
      footer = module.footer(req)

  if footer:
    template.footer.raw = footer


  # Setup sidebar text.

  sidebar = ""

  if options.has_key("sidebar"):
    sidebar = options["sidebar"]

  else:
    target = _search(req,settings,"_sidebar.html")

    if target:
      sidebar = vampire.loadTemplate(target,"vampire:node")

    if sidebar:
      collector = []
      sidebar.body._renderContent(collector)
      sidebar = ''.join(collector)

  template.rightColumn.raw = sidebar

  # Setup stylesheets.

  def renderStylesheet(node,data):
    media,href = data
    if href.find('%(') != -1:
      node.atts["href"] = cgi.escape(href%settings)
    else:
      node.atts["href"] = cgi.escape(href)
    node.atts["media"] = media

  STYLESHEETS_2COLUMN = (
   ( "screen",	"%(styles_home)s/two_column.css" ),
   ( "print",	"%(styles_home)s/print_media.css" ),
  )

  STYLESHEETS_3COLUMN = (
   ( "screen",	"%(styles_home)s/three_column.css" ),
   ( "print",	"%(styles_home)s/print_media.css" ),
  )

  if sidebar:
    template.stylesheet.repeat(renderStylesheet,STYLESHEETS_3COLUMN)
  else:
    template.stylesheet.repeat(renderStylesheet,STYLESHEETS_2COLUMN)


def handler_html(req):

  # Check to see if a HTML file actually exists at
  # the location which is the target of the request.

  if not os.path.exists(req.filename):
    return apache.DECLINED

  # Load file as a template object.

  template = vampire.loadTemplate(req.filename,"vampire:node")

  # Add in layout elements.

  layout_html(req,template)

  # Render the template and write out the response.

  req.content_type = "text/html"
  req.send_http_header()

  req.write(template.render())

  return apache.OK
