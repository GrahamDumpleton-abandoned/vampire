from mod_python import apache

import os

# Default handler for PDF.

def handler_pdf(req):

  # Check for existance of RML source file.

  path = os.path.splitext(req.filename)[0] + ".rml"

  if not os.path.exists(path):
    return apache.DECLINED

  # Create the document.

  import trml2pdf

  content = trml2pdf.parseString(file(path,'r').read())

  # Return the rendered page content.

  req.content_type = "application/pdf"
  req.headers_out['Content-Length'] = str(len(content))

  # Internet Explorer chokes on this with PDFs.
  #req.headers_out['Pragma'] = 'no-cache' 
  #req.headers_out['Cache-Control'] = 'no-cache' 
  #req.headers_out['Expires'] = '-1' 

  req.send_http_header()
  req.write(content)

  return apache.OK

# Default handler for RML.

def handler_rml(req):
  if os.path.exists(req.filename):
    return apache.HTTP_NOT_FOUND
  return apache.DECLINED
