# COPYRIGHT 2004-2005 DUMPLETON SOFTWARE CONSULTING PTY LIMITED

from mod_python import apache

import xmlrpclib
import sys

def serviceRequest(req,callback):

  if req.method != "POST":
    raise apache.SERVER_RETURN, apache.HTTP_METHOD_NOT_ALLOWED

  if not req.headers_in.has_key("content-type") \
      or req.headers_in["content-type"] != "text/xml":
    raise apache.SERVER_RETURN, apache.HTTP_BAD_REQUEST

  content = req.read(int(req.headers_in["content-length"]))

  params,method = xmlrpclib.loads(content)

  try:
    response = callback(req,method,params)
    response = (response,)
    response = xmlrpclib.dumps(response,methodresponse=1)
  except xmlrpclib.Fault,fault:
    response = xmlrpclib.dumps(fault)
  except:
    response = xmlrpclib.dumps(
      xmlrpclib.Fault(1,"%s:%s" % (sys.exc_type,sys.exc_value)))

  req.content_type = "text/xml"

  req.headers_out['Content-Length'] = str(len(response)) 

  req.headers_out['Pragma'] = 'no-cache'
  req.headers_out['Cache-Control'] = 'no-cache'
  req.headers_out['Expires'] = '-1'

  req.send_http_header()

  req.write(response)

  return apache.OK
