from mod_python import apache, util, Session

import vampire
import posixpath
import os


# The "loginhandler()" method is special and overrides
# the user login authentication mechanism. That is, it
# replaces use of the basic authentication mechanism
# with a session based mechanism with login being done
# through a HTML form. Note that it is necessary for it
# to be specified in the Vampire configuration file in
# order for it to be used.

def loginhandler(req):

  config = vampire.loadConfig(req,".vampire")

  if req.uri == config.get("Access","login_page"):
    return apache.OK

  # Load the session object.

  req.session = Session.Session(req)

  # If no "username" attribute defined in session,
  # assume that this is a new session.

  if not req.session.get("username",None):

    # Remember original target of request.

    req.session["next"] = req.uri

    # Redirect to the login page.

    req.session.save()

    util.redirect(req,config.get("Access","login_page"))

  # Turn off caching of all pages accessed through
  # private area which required authentication. This
  # ensures that browser doesn't keep hold of them or
  # any intermediate proxy cache. Lets hope this doesn't
  # trigger the Internet Exploder caching problem with
  # PDFs. :-(

  req.headers_out['Pragma'] = 'no-cache'
  req.headers_out['Cache-Control'] = 'no-cache'
  req.headers_out['Expires'] = '-1'


class UserDatabase:

  USERS = {
    "mickey": {
      "password": "mouse",
      "profile" : {
        "fullname": "Mickey Mouse",
        "groups": [ "PUBLIC", "ADMIN" ],
      },
    },
    "porky": {
      "password": "pig",
      "profile": {
        "fullname": "Porky Pig",
        "groups": [ "PUBLIC" ],
      }
    }
  }

  def validate(self,username,password):

    if self.USERS.has_key(username):
      if self.USERS[username]["password"] == password:
        return self.USERS[username]["profile"]


class SessionManager:

  def __init__(self,database):
    self.__database = database

  def __login__(self,req):

    # The "__login__()" method overrides the default
    # login manager specified by the "loginhandler".
    # This is because it is attached to the actual
    # object encompassing the resources being requested.
    # This ensures that the methods which implement
    # session login and session logout don't need
    # themselves to be authenticated. All this method
    # does is load the session object, but nothing else.

    req.session = Session.Session(req)

  def logout(self,req):

    # Invalidate the active session object, thereby
    # effectively logging out the users session.

    req.session.invalidate()

    # Redirect the client back to the login page.

    config = vampire.loadConfig(req,".vampire")

    util.redirect(req,config.get("Access","login_page"))

  def login(self,req,username=None,password=None):

    # Grab the configuration file containing information
    # about location of the site login and index pages.

    config = vampire.loadConfig(req,".vampire")

    # Validate that the user has access and if they do not
    # redirect them back to the login page.

    profile = self.__database.validate(username,password)

    if not profile:
      util.redirect(req,config.get("Access","login_page"))

    # Save the username in the session object. This is
    # the trigger for knowing that login was successful
    # in subsequent requests.

    req.session["username"] = username
    req.session["profile"] = profile

    # If no "next" attribute defined in session, assume
    # that location of this method was entered explicitly.

    if not req.session.has_key("next"):

      # Redirect the user to the site index page.

      req.session.save()

      util.redirect(req,config.get("Access","index_page"))

    # Retrieve page that user was originally wanting.

    next = req.session.pop("next")

    # Redirect to the original page.

    req.session.save()

    util.redirect(req,next)


database = UserDatabase()
manager = SessionManager(database)

handler = vampire.Handler(manager)
