from mod_python import apache

import os
import csv
import cgi
import time

def handler(req,mimeType):
  if mimeType == "text/plain":
    return handler_csv(req,mimeType)
  elif mimeType == "text/comma-separated-values":
    return handler_csv(req,mimeType)
  elif mimeType == "text/tab-separated-values":
    return handler_tsv(req)
  elif mimeType == "application/vnd.ms-excel":
    return handler_tsv(req)
  elif mimeType == "text/html":
    return handler_html(req)
  else:
    return apache.HTTP_BAD_REQUEST

def handler_csv(req,mimeType="text/comma-separated-values"):

  if mimeType != "text/comma-separated-values" and \
      mimeType != "application/vnd.ms-excel" and \
      mimeType != "text/plain":
    return apache.HTTP_BAD_REQUEST

  file = os.path.splitext(req.filename)[0] + ".csv"

  req.content_type = mimeType
  req.send_http_header()

  if hasattr(req,"sendfile"):
    req.sendfile(file)
  else:
    fd = open(file,'rb')
    req.write(fd.read())
    fd.close()

  return apache.OK

def handler_tsv(req):

  file = os.path.splitext(req.filename)[0] + ".csv"

  fd = open(file,'rb')
  reader = csv.reader(fd)

  req.content_type = "text/tab-separated-values"
  req.send_http_header()

  writer = csv.writer(req,dialect="excel-tab")
  for row in reader:
    writer.writerow(row)

  fd.close()

  return apache.OK

def handler_html(req):

  title = "Country Codes"

  file = os.path.splitext(req.filename)[0] + ".csv"

  mtime = os.path.getmtime(file)
  mtime = time.localtime(mtime)

  fd = open(file,'rb')
  reader = csv.reader(fd)

  req.content_type = "text/html"
  req.send_http_header()

  req.write("<html>\n")
  req.write("<head>\n")
  req.write("<title>%s</title>"%cgi.escape(title))
  req.write("</head>\n")
  req.write("<body>\n")
  req.write("<h1>%s</h1>"%cgi.escape(title))

  text = time.strftime("Updated: %a %b %e %H:%M:%S %Y",mtime)
  req.write("<p>%s</p>\n"%cgi.escape(text))

  req.write("<table>")
  req.write("<thead>")
  req.write("<tr>\n")

  row = reader.next()

  for field in row:
    req.write("<th>%s</th>\n"%cgi.escape(field))

  req.write("</tr>\n")
  req.write("</thead>\n")
  req.write("<tbody>\n")

  for row in reader:
    req.write("<tr>\n")
    for field in row:
      req.write("<td>%s</td>\n"%cgi.escape(field))
    req.write("</tr>\n")

  req.write("</tbody>\n")
  req.write("</table>\n")
  req.write("</body>\n")
  req.write("</html>\n")

  fd.close()

  return apache.OK
