from mod_python import apache

import vampire
import os


# Note that the following handler expects that the
# "tmpl" files have been compiled manually using
# "cheetah-compile". It does not invoke compilation.
#
# Also note that since Cheetah compiles in all the
# import statements explicitly, there doesn't seem to be
# any way to have it use the Vampire import mechanism
# instead when extending another Cheetah class. You thus
# cannot benefit from all the automatic reloading
# mechanisms that the Vampire import mechanism provides.
# All this also means that you should never define the
# PythonPath directive so as to fix it to "sys.path" as
# is recommended when using Vampire if you want to
# extend from Python classes stored in the document
# tree. This is because none of the Python style imports
# will then work. The auto reloading of pages themselves
# is okay though. In summary, if you change anything
# that is a base class, you would need to restart Apache.

def handler(req,**fields):

  # We only want to treat request as being a possible
  # request for a Cheetah generated template file if
  # there exists both a ".tmpl" and ".py" file.

  target = os.path.splitext(req.filename)[0]

  target_tmpl = target + ".tmpl"
  target_py = target + ".py"

  if not os.path.exists(target_tmpl) and not os.path.exists(target_py):
    return apache.DECLINED

  # Grab the module name to look for from the last part
  # of the path. This means that pages can be spread
  # across subdirectories as well.

  directory,module_name = os.path.split(target)

  # Import the module. Any coding error in the module
  # being imported is thrown back to the user. Error
  # also results if by chance the target just vanished.

  module = vampire.importModule(module_name,directory,req)

  # Ensure that there is a class defined in the module
  # of the appropriate name.

  if not hasattr(module,module_name):
    return apache.DECLINED

  # Create instance of the class.

  tmpl = getattr(module,module_name)()

  # Cache any decoded form parameters in an obvious
  # place so they are available. Note that the actual
  # mod_python form object is also cached as "req.form"
  # but the decoded form parameters would preferably be
  # used. By default decoded form parameters follow
  # structured naming convention supported by Vampire.
  # If this naming convention isn't wanted, it would
  # need to be disabled in the Apache configuration.

  req.fields = fields

  # Cache the Vampire configuration object in an obvious
  # place as well. Use the same one as defined the
  # default handlers which would have triggered use of
  # this handler in the first place.

  options = req.get_options()

  file = ".vampire"
  if options.has_key("VampireHandlersConfig"):
    file = options["VampireHandlersConfig"]
  config = vampire.loadConfig(req,file)

  req.config = config

  # Make request object available within the template.
  
  tmpl.req = req

  # Set type of content being returned if not set.

  if not req._content_type_set:
    req.content_type = "text/html"

  # Now generate the actual content and return it.

  req.send_http_header()

  req.write(tmpl.respond())

  return apache.OK


# Also link handler to that for ".html" requests. Which
# is used and thus whether REST style URLs are used or
# requests with a ".html" extension is dictated by how
# settings are defined in the Vampire configuration
# file.

handler_html = handler


# Block access to raw Cheetah files.

def handler_tmpl(req):
  if os.path.exists(req.filename):
    return apache.HTTP_NOT_FOUND
  return apache.DECLINED
