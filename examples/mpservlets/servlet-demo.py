from mod_python.servlet import HTMLPage

class Servlet(HTMLPage):
        
  title = "Hello World!"
            
  def write_content(self):
    self.writeln("Hello World!")
