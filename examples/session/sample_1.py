from mod_python import apache

CONTENT = """
<html>
<head>
<title>Handler Sample</title>
</head>
<body>

<h1>Handler Sample</h1>

<p>
Hello %(fullname)s.
</p>
<p>
You should probably go back to the <a href="index.html">index</a> page now.
</p>

</body>
</html>
"""

def handler_html(req):
  req.content_type = "text/html"
  req.send_http_header()

  print >> req, CONTENT % req.session["profile"]

  return apache.OK
