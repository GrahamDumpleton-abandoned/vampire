import cgi

__auth_realm__ = "Blood Bank"
__auth__ = { "donor": "blood" }

class Handler:

  def __call__(self,req,message=""):
    if not message: message = "Give Blood!"
    req.content_type = "text/html"
    req.send_http_header()
    req.write("<html><body>")
    req.write(cgi.escape(message))
    req.write("</body></html>")

handler_html = Handler()
