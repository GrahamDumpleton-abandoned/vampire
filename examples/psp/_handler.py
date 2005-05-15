from mod_python import apache

import os
import sys
import vampire

# We can't use the "import" statement for "psp" because
# of strange problems in mod_python module loader.
# Namely, if "import" is used and PythonHandler is
# defined elsewhere as "mod_python.psp" and it gets
# loaded before this code, the "psp" module can not then
# be found. Instead use the mod_python module loader
# itself as then it always works.

#from mod_python import psp
psp = apache.import_module("mod_python.psp")


# Handler for serving up PSP files. The handler will
# maintain compatibility with how standard PSP works,
# except that the ".psp" extension isn't used. Depending
# on how Vampire configuration is setup, either ".html"
# extension is used, or REST style URL with no actual
# extension.

def handler(req):

  # We only want to treat request as being a possible
  # request for a PSP template file if there exists a
  # ".psp" file.

  path = os.path.splitext(req.filename)[0] + ".psp"

  if not os.path.exists(path):
    return apache.DECLINED

  # PSP template files are always HTML files.

  req.content_type = "text/html"

  # Trigger parsing of the PSP file. The file cache
  # for PSP files is still being used here.

  template = psp.PSP(req,filename=path)

  code = template.code

  # Check whether the code is trying to make use of
  # sessions. If it is, first look for session created
  # externally and stored in the req object. If this
  # doesn't exist only then create a session object.

  session = None

  if "session" in code.co_names:
    if hasattr(req,"session"):
      session = req.session
    else:
      session = Session.Session(req)

  # Check whether the code is trying to make use of the
  # form object. If it is, use the form object created
  # by Vampire.

  form = None

  if "form" in code.co_names:
    vampire.processForm(req)
    form = req.form

  # Check whether the code is trying to make use of the
  # form fields. If it is, put the actual form fields
  # into the execution environment as well. This is an
  # addition on top of what original PSP did.

  fields = {}

  if "fields" in code.co_names:
    fields = vampire.processForm(req)

  # Create PSP interface object for compatibility.

  interface = psp.PSPInterface(req,template.filename,form)

  # Build up the execution environment to be used.
  # Defaults from Vampire configuration are also pushed
  # into the environment so that these can be used. If
  # user defined settings are placed into the "DEFAULT"
  # section of configuration file, these will also be
  # available.

  environ = globals().copy() 

  config = vampire.loadConfig(req,".vampire")
  environ.update(config.defaults())

  environ["req"] = req
  environ["session"] = session
  environ["form"] = form
  environ["fields"] = fields
  environ["psp"] = interface

  # Now execute the actual page to handle the request.

  try:

    try:
      exec code in environ

      req.flush()

      # Always ensure that session object is saved.

      if session is not None:
	session.save()

    except: 
      et,ev,etb = sys.exc_info()

      # Use error page to display details of error if
      # an actual error page was supplied.

      if interface.error_page:
	template.error_page.run({"exception":(et,ev,etb)})

      else:
	raise et,ev,etb

  finally:
    if session is not None:
      session.unlock()


# Also link handler to that for ".html" requests. Which
# is used and thus whether REST style URLs are used or
# requests with a ".html" extension is dictated by how
# settings are defined in the Vampire configuration
# file.

handler_html = handler                                                          


# Block access to raw PSP files.

def handler_psp(req):
  if os.path.exists(req.filename):
    return apache.HTTP_NOT_FOUND
  return apache.DECLINED
