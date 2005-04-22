from mod_python import apache

import vampire
import os

# To ensure that startup cost of loading "netsvc" module
# is done as early as possible instead of upon first
# request, it could be loaded explicitly using the
# "PythonImport" directive in Apache configuration file.

import netsvc


# Need to explicitly check for module reloads and only
# initialise dispatcher and exchange client the first
# time the module is reloaded.

if not globals().has_key("_dispatcher"):

  msg = "netsvc: Starting dispatcher (%d)" % os.getpid()
  apache.log_error(msg,apache.APLOG_NOTICE)

  _dispatcher = netsvc.Dispatcher()

  config = vampire.loadConfig(__req__,".vampire")

  _host = config.get("Exchange","host")
  _port = int(config.get("Exchange","port"))
  _delay = float(config.get("Exchange","delay"))

  msg = "netsvc: Exchange (%s:%d)" % (_host,_port)
  apache.log_error(msg,apache.APLOG_NOTICE)

  _exchange = netsvc.Exchange(netsvc.EXCHANGE_CLIENT)
  _exchange.connect(_host,_port,_delay)

  del config

  # We want to try and shutdown the dispatcher when
  # Apache is being shutdown or Apache may not shutdown
  # promptly and it may decide to just kill the
  # processes rather than allow them to shutdown
  # gracefully.

  def _shutdown():
    msg = "netsvc: Stopping dispatcher (%d)" % os.getpid()
    apache.log_error(msg,apache.APLOG_NOTICE)
    _dispatcher.task().stop()
    _dispatcher.task().wait()

  __req__.server.register_cleanup(__req__,_shutdown,())

  _dispatcher.task().start()


# In case the code is modified and the module reloaded,
# need to ensure that existing dispatcher and exchange
# client instances are preserved. Do this by defining
# the special "__clone__()" method and copying them from
# the original module into the new.

def __clone__(module):
  module._dispatcher = _dispatcher
  module._exchange = _exchange
