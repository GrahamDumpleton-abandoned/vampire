#!/usr/bin/env python

import docutils.writers.html4css1

PREFIX = """
<div id="pageWrapper">
<div id="masthead" class="inside">
<!-- masthead content begin -->
<h1 vampire:node="con:masthead"></h1>
<!-- masthead content end -->
</div>
<!-- horizontal nav begin -->
<div class="hnav" vampire:node="con:hnav"></div>
<!-- horizontal nav end -->
<div id="outerColumnContainer">
<div id="innerColumnContainer">
<div id="SOWrap">
<div id="middleColumn">
<div class="inside">

<div vampire:node="-con:body">
<!-- content begin -->

"""

SUFFIX = """
<!-- content end -->
</div>

</div>
</div>
<div id="leftColumn">
<div class="inside">
<!--- left column begin -->
<!-- vertical nav begin -->
<div class="vnav" vampire:node="con:vnav"></div>
<!-- vertical nav end -->
<!--- left column end -->
</div>
</div>
</div>
<div id="rightColumn">
<div class="inside">
<!--- right column begin -->
<div vampire:node="-con:rightColumn"></div>
<!--- right column end -->
</div>
</div>
<div class="clear mozclear"></div>
</div>
</div>
<div id="footer" class="inside">
<!-- footer begin -->
<p style="margin:0;" vampire:node="con:footer"></p>
<!-- footer end -->
</div>
</div>

"""

STYLESHEET = """
<style vampire:node="rep:style"></style>
<link vampire:node="rep:stylesheet" rel="stylesheet" href="%s" type="text/css" />
<script vampire:node="rep:script"></script>
"""

class HTMLFragmentTranslator(docutils.writers.html4css1.HTMLTranslator):

  stylesheet_link = STYLESHEET

  def __init__(self,*params,**kwargs):
    docutils.writers.html4css1.HTMLTranslator.__init__(self,*params,**kwargs)
    self.body_prefix.append(PREFIX)
    self.body_suffix.insert(0,SUFFIX)

class HTMLFragmentWriter(docutils.writers.html4css1.Writer):

  def __init__(self,*params,**kwargs):
	  docutils.writers.html4css1.Writer.__init__(self,*params,**kwargs)
	  self.translator_class = HTMLFragmentTranslator

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline, default_description


description = ('Generates (X)HTML documents from standalone reStructuredText '
               'sources.  ' + default_description)

writer = HTMLFragmentWriter()

publish_cmdline(writer=writer, description=description)
