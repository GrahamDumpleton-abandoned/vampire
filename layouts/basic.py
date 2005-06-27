from mod_python import apache

import os
import sys

import vampire


# Base class for object handlers which make use of
# HTMLTemplate via the Vampire template loading and
# caching mechanism. Note that an instance of the
# template class, whether it be the base class or a
# derived class, must be created. This can be done
# by wrapping the class with "vampire.Instance()".

class Template:

  # Default list of allowed request method types.

  allowed_methods = [ "GET", "POST" ]

  # Default name of the node used in HTML to denote
  # special elements with associated HTMLTemplate
  # compiler directives.

  node_name = "vampire:node"

  # Default for the type of content being returned.

  content_type = "text/html"

  # Default for whether caching of response should be
  # disabled or not.

  no_cache = False

  # Default name of config file to automatically load
  # for each request.

  config_file = None

  def __init__(self,req):

    # Save away a copy of the request object. The
    # request object will be supplied at the point of
    # construction by the "vampire.Instance()" wrapper
    # when it creates an instance of this class for each
    # received request.

    self.req = req

  def loadTemplate(self):

    # Load the page template specific to the request.

    filename = os.path.splitext(self.req.filename)[0] + ".html"

    if not os.path.exists(filename):
      raise apache.SERVER_RETURN, apache.DECLINED

    self.template = vampire.loadTemplate(filename,self.node_name)

  def __deliverResponse(self):

    # Render the page template into actual content.

    content = self.template.render()

    # Set up returned content type for response.

    self.req.content_type = self.content_type

    # Disable caching of response if required.

    if self.no_cache:
      self.req.headers_out['Pragma'] = 'no-cache' 
      self.req.headers_out['Cache-Control'] = 'no-cache' 
      self.req.headers_out['Expires'] = '-1' 

    # Flush out the HTTP request headers.

    self.req.send_http_header()

    # Write out the actual page content.

    self.req.write(content)

  def renderTemplate(self):

    # Should be overridden in a derived class. It is
    # recommended that a derived implementation always
    # call a base class version of this method as its
    # final action. This will allow for base classes to
    # do common page template manipulation to fill in
    # fields. If a derived class needs to return an
    # error, it should raise as a apache.SERVER_RETURN
    # exception, with HTTP error code as argument.

    pass

  def __call__(self):

    # Check that request method type is allowed.

    if hasattr(self.req,"allow_methods"):
      self.req.allow_methods(self.allowed_methods)

    if self.req.method not in self.allowed_methods:
      raise apache.SERVER_RETURN, apache.HTTP_METHOD_NOT_ALLOWED

    # Load in specified configuration file.

    if self.config_file:
      self.config = vampire.loadConfig(self.req,self.config_file)

    # Load the appropriate page template file.

    self.loadTemplate()

    # Call the derived class method for processing of
    # request and filling out of page template content.
    # Because "vampire.executeHandler()" is used to call
    # the class method, a derived class method may
    # define arguments which correspond to any form
    # parameters which may have been supplied with the
    # request.

    vampire.executeHandler(self.req,self.renderTemplate)

    # Deliver up the response to the request.

    self.__deliverResponse()


handler_html = vampire.Instance(Template)
