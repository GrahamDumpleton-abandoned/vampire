import vampire
import cgi

class Handler:

  def __init__(self,req):
    self.__req = req

  def __call__(self,message=""):
    if not message: message = "Give Blood!"
    self.__req.content_type = "text/html"
    self.__req.send_http_header()
    self.__req.write("<html><body>")
    self.__req.write(cgi.escape(message))
    self.__req.write("</body></html>")

handler_html = vampire.Instance(Handler)
