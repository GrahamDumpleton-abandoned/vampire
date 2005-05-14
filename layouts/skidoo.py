from mod_python import apache

import vampire
import cgi
import os

directory = os.path.split(__file__)[0]
basic = vampire.importModule("basic",directory,__req__)


# Extension to basic object handler for template which
# massages HTML with appropriate marked elements into a
# two or three column page incorporating navigation bar,
# page links and sidebar.

class Template(basic.Template):

  # Name of configuration file to be loaded.

  config_file = ".vampire"

  # Defaults for various page template components.

  masthead = None
  navbar = None
  links = None
  footer = None
  sidebar = None

  def __cacheSettings(self):

    # Cache configuration settings for later use.

    self.__settings = {}

    for key,value in self.config.items("Settings"):
      self.__settings[key] = value

  def __searchPlugin(self,file):

    # Searches for plugin associated with target of
    # request by first looking for a file with name
    # formed by adding "file" to end of basename of
    # target of request. If this isn't found, then
    # search is made for "file" back up the directory
    # hierarchy until the document root is reached.
    # It is expected that "document_root" be defined
    # as a setting in the configuration file.

    target = os.path.splitext(self.req.filename)[0] + file
    if os.path.exists(target):
      return target

    document_root = self.__settings["document_root"]

    directory = os.path.dirname(self.req.filename)
    while len(directory) >= len(document_root):
      target = os.path.join(directory,file)
      if os.path.exists(target):
	return target
      directory = os.path.split(directory)[0]

    return None

  def __importPlugin(self,file):

    target = self.__searchPlugin(file)

    if target:
      directory = os.path.dirname(target)
      name = os.path.splitext(os.path.basename(target))[0]
      return vampire.importModule(name,directory,self.req)

  def __renderMasthead(self):

    # Render page template masthead.

    masthead = ""

    if self.masthead is not None:
      masthead = self.masthead

    else:
      module = self.__importPlugin("_masthead.py")

      if module:
	masthead = module.masthead(self.req)

    if masthead:
      self.template.masthead.raw = masthead

  def __formatNavigation(self,links):

    # Format HTML for nagivation bar.

    output = []

    output.append('<ul>')

    for label,target in links:
      if target.find('%(') != -1:
	target = target % self.__settings
      target = cgi.escape(target)
      label = cgi.escape(label)

      output.append('<li><a href="%s">%s</a>' % (target,label))
      output.append('<span class="divider"> : </span>')

    output.append('</ul>')

    return "".join(output)

  def __renderNavigation(self):

    # Render page template navigation bar.

    navbar = []

    if self.navbar is not None:
      navbar = self.navbar

    else:
      module = self.__importPlugin("_navbar.py")

      if module:
	navbar = module.navbar(self.req)

    if navbar:
      self.template.hnav.raw = self.__formatNavigation(navbar)

  def __formatLinks(self,groups):

    # Format HTML for links.

    output = []

    for name,links in groups:
      output.append('<h3>')
      output.append(cgi.escape(name))
      output.append('</h3>\n')

      output.append('<ul>')

      for label,target in links:
	if target.find('%(') != -1:
	  target = target % self.__settings
	target = cgi.escape(target)
	label = cgi.escape(label)

	output.append('<li><a href="%s">%s</a>' % (target,label))

      output.append('</ul>\n')

    return "".join(output)

  def __renderLinks(self):

    # Render page template links.

    links = []

    if self.links is not None:
      links = self.links

    else:
      module = self.__importPlugin("_links.py")

      if module:
	links = module.links(self.req)

    if links:
      self.template.vnav.raw = self.__formatLinks(links)

  def __renderFooter(self):

    # Render page template footer.

    footer = ""

    if self.footer is not None:
      footer = self.footer

    else:
      module = self.__importPlugin("_footer.py")

      if module:
	footer = module.footer(self.req)

    if footer:
      self.template.footer.raw = footer

  def __renderSidebar(self):

    # Render page template sidebar.

    sidebar = ""

    if self.sidebar is not None:
      sidebar = self.sidebar

    else:
      target = self.__searchPlugin("_sidebar.html")

      if target:
	sidebar = vampire.loadTemplate(target,self.node_name)

      if sidebar:
	collector = []
	sidebar.body._renderContent(collector)
	sidebar = ''.join(collector)

    self.template.rightColumn.raw = sidebar

  def __renderHeader(self):

    # Fillin details of appropriate style sheet.

    def renderStylesheet(node,data):
      media,href = data
      if href.find('%(') != -1:
	node.atts["href"] = cgi.escape(href%self.__settings)
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

    if self.template.rightColumn.raw:
      self.template.stylesheet.repeat(renderStylesheet,STYLESHEETS_3COLUMN)
    else:
      self.template.stylesheet.repeat(renderStylesheet,STYLESHEETS_2COLUMN)

  def renderTemplate(self):

    # Cache configuration settings.

    self.__cacheSettings()

    # Render internal elements of page template.

    self.__renderMasthead()
    self.__renderNavigation()
    self.__renderLinks()
    self.__renderFooter()
    self.__renderSidebar()
    self.__renderHeader()

    # Trigger base class method in case it needs to do
    # any additional work.

    basic.Template.renderTemplate(self)


handler_html = vampire.Instance(Template)
