import vampire
import os

def masthead(req):
  config = vampire.loadConfig(req,'.vampire')
  root = config.defaults()['__config_root__']

  directory = os.path.dirname(req.filename)
  banner = directory[len(root):]
  if banner[:1] == '/':
    banner = banner[1:]

  if not banner:
    return 'PROJECTS / VAMPIRE'

  else:
    banner = "VAMPIRE/" + banner
    banner = banner.upper()
    banner = banner.split('/')[-3:]
    banner = '/'.join(banner)
    banner = banner.replace('/',' / ')
    return banner
