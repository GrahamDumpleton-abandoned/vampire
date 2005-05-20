import vampire

class _Object:

  def method1(self,req):
    req.content_type = "text/plain"
    req.send_http_header()
    req.write("method1()")

  def method2(self,req):
    req.content_type = "text/plain"
    req.send_http_header()
    req.write("method2()")

  def __call__(self,req):
    req.content_type = "text/plain"
    req.send_http_header()
    req.write("__call__()")

_object = _Object()

handler = vampire.Handler(_object)
