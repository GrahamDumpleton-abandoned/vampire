import vampire

# The "vampire.PathInfo()" class can be used to wrap a
# method so that any additional path information beyond
# that which was required to match the original method
# will be accumulated and passed in to the method as a
# special parameter. The default name of the parameter
# is "path" but can be changed at the point the wrapper
# is constructed. If wrapping a class method, it must be
# done from inside of the constructor. The special "req"
# parameter can still be used to get access to the
# request object and other form parameters can also be
# specified. If a form parameter is supplied with the
# request which is the same as the parameter the path is
# being passed through, the path details will override
# the form value supplied with the request. There is no
# equivalent functionality in mod_python.publisher for
# this feature.

def _method1(path):
  return "method1()",path

# URL: "/method1/1/2/3".
# Result: path="/1/2/3".

method1 = vampire.PathInfo(_method1)

def _method2(req,path):
  return "method2()",path

# URL: "/method2/1/2/3".
# Result: path="/1/2/3".

method2 = vampire.PathInfo(_method2)

def _method3(xpath):
  return "_method3()",xpath

# URL: "/method3/1/2/3".
# Result: xpath="/1/2/3".

method3 = vampire.PathInfo(_method3,"xpath")

def _method4(req,xpath):
  return "_method4()",xpath

# URL: "/method4/1/2/3".
# Result: xpath="/1/2/3".

method4 = vampire.PathInfo(_method4,"xpath")

def _method5(path,param1,param2="default"):
  return "method5()",path,param1,param2

# URL: "/method5/1/2/3?param1=1".
# Result: path="/1/2/3", param1="1", param2="default".

# URL: "/method5/1/2/3?param1=1&param2=2".
# Result: path="/1/2/3", param1="1", param2="2".

method5 = vampire.PathInfo(_method5)

def _method6(req,path,param1,param2="default"):
  return "method6()",path,param1,param2

# URL: "/method6/1/2/3?param1=1".
# Result: path="/1/2/3", param1="1", param2="default".

# URL: "/method6/1/2/3?param1=1&param2=2".
# Result: path="/1/2/3", param1="1", param2="2".

method6 = vampire.PathInfo(_method6)

class Class1:

  def __init__(self):
    self.method1 = vampire.PathInfo(self._method1)

  def _method1(self,path):
    return "Class1._method1",path

# URL: "/class1/method1/1/2/3".
# Result: path="/1/2/3".

class1 = Class1()

