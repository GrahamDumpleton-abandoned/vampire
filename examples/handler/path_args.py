import vampire

class _Object:

  def __init__(self):
    self.method1 = vampire.PathArgs(self._method1)
    self.method2 = vampire.PathArgs(self._method2)
    self.method3 = vampire.PathArgs(self._method3)

  def _method1(self,year,month,day="0"):
    return "_method1",year,month,day

  def _method2(self,req,year,month,day="0"):
    return "_method2",req.uri,year,month,day

  def _method3(self,req,year,mon,day="0",*kwlist):
    return "_method3",req.uri,year,mon,day,kwlist

_object = _Object()

handler = vampire.Publisher(_object)
