from mod_python import apache

import StringIO

# Default handler.

def _colors(canvas):
  from reportlab.lib import colors
  from reportlab.lib.units import inch
  black = colors.black
  y = 300; x = 100
  dy=inch*3/4.0; dx=inch*5.5/5; w=h=dy/2; rdx=(dx-w)/2
  rdy=h/5.0; texty=h+2*rdy
  canvas.setFont("Helvetica",10)
  for [namedcolor, name] in (
      [colors.lavenderblush, "lavenderblush"],
      [colors.lawngreen, "lawngreen"],
      [colors.lemonchiffon, "lemonchiffon"],
      [colors.lightblue, "lightblue"],
      [colors.lightcoral, "lightcoral"]):
    canvas.setFillColor(namedcolor)
    canvas.rect(x+rdx, y+rdy, w, h, fill=1)
    canvas.setFillColor(black)
    canvas.drawCentredString(x+dx/2, y+texty, name)
    x = x+dx
  y = y + dy; x = 100
  for rgb in [(1,0,0), (0,1,0), (0,0,1), (0.5,0.3,0.1), (0.4,0.5,0.3)]:
    r,g,b = rgb
    canvas.setFillColorRGB(r,g,b)
    canvas.rect(x+rdx, y+rdy, w, h, fill=1)
    canvas.setFillColor(black)
    canvas.drawCentredString(x+dx/2, y+texty, "r%s g%s b%s"%rgb)
    x = x+dx
  y = y + dy; x = 100
  for cmyk in [(1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1), (0,0,0,0)]:
    c,m,y1,k = cmyk
    canvas.setFillColorCMYK(c,m,y1,k)
    canvas.rect(x+rdx, y+rdy, w, h, fill=1)
    canvas.setFillColor(black)
    canvas.drawCentredString(x+dx/2, y+texty, "c%s m%s y%s k%s"%cmyk)
    x = x+dx
  y = y + dy; x = 100
  for gray in (0.0, 0.25, 0.50, 0.75, 1.0):
    canvas.setFillGray(gray)
    canvas.rect(x+rdx, y+rdy, w, h, fill=1) 
    canvas.setFillColor(black)
    canvas.drawCentredString(x+dx/2, y+texty, "gray: %s"%gray)
    x = x+dx 

def handler_pdf(req):

  # Create the document.

  output = StringIO.StringIO()

  from reportlab.pdfgen import canvas
  c = canvas.Canvas(output)
  _colors(c)
  c.showPage()
  c.save()

  # Return the rendered page content.

  content = output.getvalue()

  req.content_type = "application/pdf"
  req.headers_out['Content-Length'] = str(len(content))

  # Internet Explorer chokes on this with PDFs.
  #req.headers_out['Pragma'] = 'no-cache' 
  #req.headers_out['Cache-Control'] = 'no-cache' 
  #req.headers_out['Expires'] = '-1' 

  req.send_http_header()
  req.write(content)

  return apache.OK
