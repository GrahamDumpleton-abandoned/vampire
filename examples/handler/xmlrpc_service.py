# This file exhibits how an XML-RPC service can be
# constructed by wrapping an existing object. Both
# methods and data are automatically exported. Thus, if
# you don't want something to be exposed make sure the
# name is prefixed with an underscore.
#
# Note that if the first parameter of an exposed method
# is "req", that parameter will be passed the mod_python
# request object with the actual XML-RPC parameters then
# being passed in subsequent parameters.

import vampire

class Object1:

  def method1(self):
    return "Object1.method1()"

class Object2:

  def __init__(self):
    self.object1 = Object1()

    self.string1 = "str"
    self.dict1 = {"1":2}
    self.list1 = [1,2]
    self.tuple1 = (1,2)
    self.int1 = 1
    self.float1 = 1.1

  def method1(self):
    return "Object2.method1()"

  def method2(self,req):
    return "Object2.method2()",req.uri

  def method3(self,data):
    return "Object3.method3()",data

  def method4(self,req,data):
    return "Object4.method4()",req.uri,data

_object2 = Object2()

handler = vampire.Service(_object2)
