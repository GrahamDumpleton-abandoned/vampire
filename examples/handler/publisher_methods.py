import vampire

class _Object:

  def __init__(self):
    self.value1 = "value1"

  def method1(self):
    return "method1()"

  def method2(self,req):
    req.content_type = "text/plain"
    req.send_http_header()
    req.write("method2()")

  def __call__(self):
    return "__call__()"

_object = _Object()

handler = vampire.Publisher(_object)
