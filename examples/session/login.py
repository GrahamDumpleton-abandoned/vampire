from mod_python import apache, util, Session

import vampire
import posixpath
import os


# Dummy user database.

_users = { "mickey": "mouse" }


# The "__login__()" method is special and overrides for
# this file the user login authentication mechanism.
# That is, it replaces use of the basic authentication
# mechanism with a session based mechanism with login
# being done through a HTML form. Because it is also
# referenced by the "__login__" setting in the
# "Handlers" section of the Vampire configuration it
# actually then also gets applied to all requests within
# the directory.

def __login__(req):

  # Load the session object.

  req.session = Session.Session(req)

  # If no "username" attribute defined in session,
  # assume that this is a new session.

  if not req.session.get("username",None):

    # Remember original target of request.

    req.session["next"] = req.uri

    # Redirect to the login page.

    req.session.save()

    config = vampire.loadConfig(req,".vampire")
    util.redirect(req,config.get("Login","login"))

  # Turn off caching of all pages accessed through
  # private area which required authentication. This
  # ensures that browser doesn't keep hold of them or
  # any intermediate proxy cache. Lets hope this doesn't
  # trigger the Internet Exploder caching problem with
  # PDFs. :-(

  req.headers_out['Pragma'] = 'no-cache'
  req.headers_out['Cache-Control'] = 'no-cache'
  req.headers_out['Expires'] = '-1'


def handler_html(req,event="Login",username=None,password=None):

  # This version of "__login__()" actually overrides
  # that specified above because it is attached to the
  # actual handler for the resource being requested.
  # Its presence therefore ensures that authentication
  # isn't required to access the login page.

  def __login__(req):

    # Load the session object, but do nothing else.

    req.session = Session.Session(req)

  # Is logout being explicitly requested.

  if event == "Logout":

    # Invalidate the session.

    req.session.invalidate()

    # Redirect to the login page.

    config = vampire.loadConfig(req,".vampire")
    util.redirect(req,config.get("Login","login"))

  # If no "next" attribute defined in session, assume
  # that location of login page was entered explicitly.

  if not req.session.has_key("next"):

    # Save index page as target of request so that after
    # login, user will be directed to that page.

    config = vampire.loadConfig(req,".vampire")
    req.session["next"] = config.get("Login","index")

    # Redirect back onto ourselves.

    req.session.save()

    util.redirect(req,req.uri)

  # If login has not yet occurred or incorrect login
  # details, need to display the login page.

  if not username or not password or \
      _users.get(username,None) != password:

    # Caching of the login page should be disabled else
    # strange things can happen due to login page being
    # accessed as both GET and POST requests.

    req.content_type = "text/html"
    req.headers_out['Pragma'] = 'no-cache'
    req.headers_out['Cache-Control'] = 'no-cache'
    req.headers_out['Expires'] = '-1'
    req.send_http_header()

    # Send back content of the login page.

    req.sendfile(req.filename)

    return apache.OK

  # Save the username in the session object. This is
  # the trigger for knowing that login was successful
  # in subsequent requests.

  req.session["username"] = username

  # Retrieve page that user was originally wanting.

  next = req.session.pop("next")

  # Redirect to the original page.

  req.session.save()

  util.redirect(req,next)
