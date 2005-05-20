def handler_html(req):
  req.content_type = "text/html"
  req.send_http_header()
  req.write("<html><body>Give Blood!</body></html>")

def handler_txt(req):
  req.content_type = "text/plain"
  req.send_http_header()
  req.write("Give Blood!\n")
