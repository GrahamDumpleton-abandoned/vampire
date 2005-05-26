#!/usr/bin/env python

import docutils.writers.html4css1

STYLESHEET = """
<style vampire:node="rep:style"></style>
<link vampire:node="rep:stylesheet" rel="stylesheet" href="%s" type="text/css" />
<script vampire:node="rep:script"></script>
"""

BODY_PREFIX = """
<div vampire:node="-con:prefix"></div>
<div vampire:node="-con:body">

<!-- content begin -->

"""

BODY_SUFFIX = """

<!-- content end -->

</div>
<div vampire:node="-con:suffix"></div>
"""

class HTMLFragmentTranslator(docutils.writers.html4css1.HTMLTranslator):

  stylesheet_link = STYLESHEET

  def __init__(self,*params,**kwargs):
    docutils.writers.html4css1.HTMLTranslator.__init__(self,*params,**kwargs)
    self.body_prefix.append(BODY_PREFIX)
    self.body_suffix.insert(0,BODY_SUFFIX)

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
