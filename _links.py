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
  _links = module._links

_package = []

_package.append(("README","README.html"))
_package.append(("LICENSE","LICENSE.html"))
_package.append(("PATCHES","PATCHES.html"))
_package.append(("CHANGES","CHANGES.html"))
_package.append(("CREDITS","CREDITS.html"))

_links.append(("Package",_package))

def links(req):
  return _links
