from mod_python import apache

import os
import string
import cgi

# Handler for virtual directory.

export = [ ".diff", ".html", ".psp", ".py", ".rml", ".vampire" ]

def handler(req):

  # Determine name of source file to view.

  if req.path_info == "":
    return apache.HTTP_BAD_REQUEST
  elif req.path_info == "/":
    return apache.HTTP_BAD_REQUEST
  else:
    name = req.path_info[1:]

  # Don't bother with files that don't exist.

  root = os.path.dirname(req.filename)
  path = os.path.join(root,name)

  if not os.path.exists(path):
    return apache.HTTP_NOT_FOUND

  # Block access to files we don't want visible.

  extn = os.path.splitext(name)[1]

  if not extn in export:
    return apache.HTTP_FORBIDDEN

  # Open the file for input.

  file = open(path,'r')

  # Return the rendered page content.

  req.content_type = "text/html"
  req.headers_out['Pragma'] = 'no-cache' 
  req.headers_out['Cache-Control'] = 'no-cache' 
  req.headers_out['Expires'] = '-1' 

  req.write("<html>\n")
  req.write("<head>\n")
  req.write("<title>File: ")
  req.write(cgi.escape(name))
  req.write("</title>\n")
  req.write("</head>\n")
  req.write("<body>\n")
  req.write("<pre>")
  req.write(cgi.escape(file.read()))
  req.write("</pre>\n")
  req.write("</body>\n")
  req.write("</html>\n")

  file.close()

  return apache.OK
