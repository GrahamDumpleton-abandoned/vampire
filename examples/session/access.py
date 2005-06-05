from mod_python import apache, util, Session

import vampire
import posixpath
import os


# The access manager is special and is used to override
# the default user login authentication mechanism of
# Vampire. That is, it replaces use of the basic
# authentication mechanism with a session based
# mechanism with login being done through a HTML form.
# For this to be used, it is still necessary for it to
# be referenced in the Vampire configuration file. The
# access manager relies on the URL of the login page
# being specified in the configuration file.

class AccessManager:

  def _unmanagedRequest(self,req):

    # Could be overridden in a derived class so as to
    # filter specific URLs for which no session object
    # needs to be created and thus also that the user is
    # not required to be logged in. This might be used
    # for image files, although one is better to disable
    # use of mod_python altogether for the particular
    # case of image files.

    return False

  def _noLoginRequired(self,req):

    # Could be overridden in a derived class so as to
    # filter specific URLs for which a user is not
    # required to be logged in. A session object would
    # still be created though. This might be used for
    # the main site index page if it encompasses a
    # separate little login box distinct from the main
    # login page and the user should be able to access
    # the main index page without logging in.

    return False

  def __call__(self,req):

    # Determine if the URL which is the target of the
    # request should be managed at all. If it is deemed
    # as unmanaged, then no session object is created at
    # all and consequently there is no requirement for a
    # user to be logged in either.

    if self._unmanagedRequest(req):
      return apache.OK

    # Load the session and store it in the request object.

    req.session = Session.Session(req)

    # Determine if the URL which is the target of the
    # request requires a user to be logged in. Note that
    # even if login is not required, a session object
    # has still been created and it can be queried or
    # updated by a request handler.

    if self._noLoginRequired(req):
      return apache.OK

    # Grab available configuration information.

    config = vampire.loadConfig(req,".vampire")

    # See if the requested URL matches that of the login
    # page. If it is, let the request through without
    # any additional checks as to whether the user is
    # already logged in. This ensures that they can
    # access the login page when they haven't yet logged
    # in. The session object is still created however,
    # so that the page could check the logged in status
    # and thus avoid presenting the login form if they
    # were already logged in and instead refer them to
    # an alternate page.

    page = config.get("Access","login_page")

    if not os.path.isabs(page):
      page = os.path.join(os.path.dirname(req.uri),page)
      page = os.path.normpath(os.path.join(page))

    if req.uri == page:
      return apache.OK

    # If no "username" attribute contained within the
    # session object, means that the user has not yet
    # logged in.

    if not req.session.get("username",None):

      # Remember original target of request.

      req.session["next"] = req.uri

      # Redirect to the login page.

      req.session.save()

      util.redirect(req,config.get("Access","login_page"))

    # Turn off caching of all pages accessed from within
    # the private area which required the user to login.
    # This ensures that browser doesn't keep hold of
    # them or any intermediate proxy cache. Lets hope
    # this doesn't trigger the Internet Exploder caching
    # problem with PDFs. :-(

    req.headers_out['Pragma'] = 'no-cache'
    req.headers_out['Cache-Control'] = 'no-cache'
    req.headers_out['Expires'] = '-1'


# This is a dodgy user database. In a real system this
# sort of information should be stored in a real
# database and provide a means of updating the profile,
# changing passwords etc etc.

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

    # Return the users profile if access is granted.

    if self.USERS.has_key(username):
      if self.USERS[username]["password"] == password:
        return self.USERS[username]["profile"]


# The login manager is what truly controls whether a
# user can login or not. The access manager which is
# linked in as the loginhandler, really only redirects
# requests to the login page when necessary. The login
# manager also looks after invalidating a session object
# when the user logs out.

class LoginManager:

  def __init__(self,database):
    self.__database = database

  def __login__(self,req):

    # The "__login__()" method overrides the default
    # login handler. This is because it is attached to
    # the actual object encompassing the resources being
    # requested. This ensures that the method which
    # implements the login process doesn't itself result
    # in redirection to the login page by accident. All
    # this method does is load the session object, but
    # nothing else.

    req.session = Session.Session(req)

  def logout(self,req):

    # Invalidate the active session object, thereby
    # effectively logging out the user.

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
    # in subsequent requests. Also cache the user profile
    # in the session object.

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


# Specify the access manager as the loginhandler. This
# file still needs to be referenced in the configuration
# file for it to become active.

loginhandler = AccessManager()

# The login manager is exported as the main handler for
# this file. The use of "vampire.Handler()" results in
# the individual methods of the login manager being
# available as separate resources with their own URLs.
# This is like it is with "mod_python.publisher" except
# that each method is still written as a basic content
# handler and not a publisher style method.

_userDatabase = UserDatabase()
_loginManager = LoginManager(_userDatabase)

handler = vampire.Handler(_loginManager)
