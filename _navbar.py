_links = []

_links.append(( "Home","%(__baseurl_rel__)s"))
_links.append(( "Projects","%(__baseurl_rel__)s/projects"))
_links.append(( "Articles","%(__baseurl_rel__)s/articles"))
_links.append(( "Downloads","%(__baseurl_rel__)s/downloads.html"))
_links.append(( "Contact","%(__baseurl_rel__)s/contact.html"))

def navbar(req):
  return _links
