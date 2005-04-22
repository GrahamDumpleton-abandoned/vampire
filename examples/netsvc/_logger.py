import netsvc
import netsvc.client
import vampire
import os

# Import startup code for dispatcher to ensure it is
# initialised and connection to exchange is created.

directory = os.path.dirname(__file__)
_gateway = vampire.importModule("_gateway",directory,__req__)


# Handler which will attempt to log all requests with
# the remote request database service.

def loghandler(req):

  # Lookup the request logging service. Abort the
  # search immediately if the service isn't already
  # registered by specifying a zero length timeout.

  registry = netsvc.client.Registry(timeout=0)
  bindings = registry.locateService("apache-logger")

  # Because we are logging requests, not serious that
  # service couldn't be found. Just means details about
  # requests for period service is not available will
  # be lost.

  if bindings != []:

    # We don't want to hang around for the response
    # whether it be successful or not either, so specify
    # zero length timeout.

    service = netsvc.client.RemoteService(bindings[0],timeout=0)

    # Because a zero length timeout is specified we will
    # get a timeout exception pretty quickly so simply
    # ignore any errors altogether.

    try:
      service.log(req.connection.remote_ip,req.request_time,
          req.the_request,req.status,req.bytes_sent)
    except:
      pass
