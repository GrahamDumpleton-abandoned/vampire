import vampire
import os

# Following determines if this is being run within the
# context of the parent web site for Vampire, and if it
# is use the links from the parent web site as well as
# any which have been added here.

current = os.path.dirname(__req__.filename)
parent = os.path.join(current,"../..")

_links = []

try:
  module = vampire.importModule("_links",parent)
except OSError:
  pass
else:
  _links = list(module._links)

_package = []

_package.append(("Overview","%(vampire_home)s/index.html"))
_package.append(("Articles","%(vampire_home)s/articles.html"))
#_package.append(("Examples","%(vampire_home)s/examples/index.html"))
_package.append(("Download","%(website_home)s/downloads.html"))
_package.append(("Installation","%(vampire_home)s/install.html"))
_package.append(("License","%(vampire_home)s/license.html"))
_package.append(("Patches","%(vampire_home)s/patches.html"))
_package.append(("Changes","%(vampire_home)s/changes.html"))
_package.append(("Credits","%(vampire_home)s/credits.html"))

_links.append(("Vampire",_package))

def links(req):
  return _links
