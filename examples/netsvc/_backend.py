import netsvc
import signal
import time
import dbm


class Logger(netsvc.Service):

  def __init__(self):
    netsvc.Service.__init__(self,"apache-logger")
    self.exportMethod(self.log)

  def log(self,remote_ip,request_time,the_request,status,bytes):
    self.publishReport("request",(remote_ip,
        netsvc.DateTime(request_time),the_request,status,bytes))
    print '%s %s "%s" %d %d' % (remote_ip,
        netsvc.DateTime(request_time),the_request,status,bytes)


class Database(netsvc.Service):

  def __init__(self,name):
    netsvc.Service.__init__(self,"simple-database")
    self._db = dbm.open(name,'c')
    self.exportMethod(self.get)
    self.exportMethod(self.put)
    self.exportMethod(self.keys)

  def get(self,key):
    return self._db[key]

  def put(self,key,value):
    self._db[key] = value

  def keys(self):
    return self._db.keys()


dispatcher = netsvc.Dispatcher()
dispatcher.monitor(signal.SIGINT)

exchange = netsvc.Exchange(netsvc.EXCHANGE_SERVER)
exchange.listen(11111)

logger = Logger()
database = Database("database")

dispatcher.run()

