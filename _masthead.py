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
    return 'GRAHAM DUMPLETON'
  else:
    banner = banner.upper()
    remainder = banner.split('/')[-3:]
    banner = '.../' + '/'.join(remainder)
    banner = banner.replace('/',' / ')
    return banner
