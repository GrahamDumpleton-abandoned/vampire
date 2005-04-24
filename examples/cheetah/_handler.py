from mod_python import apache

import vampire
import os


# Note that the following handler expects that the
# "tmpl" files have been compiled manually using
# "cheetah-compile". It does not invoke compilation.
#
# For correct operation of the Vampire mechanism for
# automatic reloading of modified modules, the Apache
# configuration file options:
#
#   PythonPath 'sys.path'
#   PythonOption VampireImportHooks On
#
# should be specified. This will ensure that base
# templates which are extended and then modified,
# will correctly result in derived templates being
# reloaded.
#
# By default this will only work where the base template
# was in the same directory as the derived. If located
# elsewhere, the Vampire configuration file should be
# updated to specify where base templates are stored by
# setting the "path" setting within the "Modules"
# section of configuration. For example:
#
#  [Modules]
#
#    layouts = %(__config_root__)s/layouts
#
#    path = %(layouts)s
#
# If multiple search directories are specified, they
# should be separated by ":".

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
