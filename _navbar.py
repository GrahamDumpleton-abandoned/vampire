import vampire
import os

# Following determines if this is being run within the
# context of the parent web site for Vampire, and if it
# is use the navigation bar from the parent web site.

current = os.path.dirname(__file__)
parent = os.path.join(current,"../..")

_links = []

try:
  module = vampire.importModule("_navbar",parent)
except OSError:
  pass
else:
  _links = list(module._links)

def navbar(req):
  return _links
