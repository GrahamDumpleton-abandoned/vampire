import vampire

class _Object:

  def __init__(self):
    self.method1 = vampire.PathInfo(self._method1)
    self.method2 = vampire.PathInfo(self._method2)
    self.method3 = vampire.PathInfo(self._method3,"xpath")
    self.method4 = vampire.PathInfo(self._method4,"xpath")
    self.method5 = vampire.PathInfo(self._method5)
    self.method6 = vampire.PathInfo(self._method6)

  def _method1(self,path):
    return "method1()",path

  def _method2(self,req,path):
    return "method2()",path

  def _method3(self,xpath):
    return "_method3()",xpath

  def _method4(self,req,xpath):
    return "_method4()",xpath

  def _method5(self,path,param1,param2="default"):
    return "method5()",path,param1,param2

  def _method6(self,req,path,param1,param2="default"):
    return "method6()",path,param1,param2

_object = _Object()

handler = vampire.Publisher(_object)
