def handler(req):
  req.content_type = "text/html"
  req.send_http_header()
  req.write("<html><body>Give Blood!</body></html>")
