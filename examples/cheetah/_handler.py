from mod_python import apache

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

def handler_html(req):

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

  module = apache.import_module(module_name,[directory])

  # Ensure that there is a class defined in the module
  # of the appropriate name.

  if not hasattr(module,module_name):
    return apache.DECLINED

  # Create instance of the class and setup request object.

  tmpl = getattr(module,module_name)()
  tmpl.req = req

  # Now generate the actual content and return it.

  req.content_type = "text/html"
  req.send_http_header()

  req.write(tmpl.respond())

  return apache.OK


# Default handler for raw Cheetah files.

def handler_psp(req):
  if os.path.exists(req.filename):
    return apache.HTTP_NOT_FOUND
  return apache.DECLINED
