_links = []

_projects = []

_projects.append(("OSE","http://ose.sourceforge.net"))
_projects.append(("Makeit","http://ose.sourceforge.net"))
_projects.append(("Vampire","%(__baseurl_rel__)s/projects/vampire"))
_projects.append(("XML-RPC","%(__baseurl_rel__)s/projects/xmlrpc"))

_links.append(("Projects",_projects))

def links(req):
  return _links
