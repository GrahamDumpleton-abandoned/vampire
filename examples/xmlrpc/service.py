# This file exhibits how an XML-RPC service can be
# constructed by wrapping an existing object. Only
# methods are automatically exported, data is not. Even
# so, ensure that data is prefixed with an underscore in
# case a decision is made to export data automatically
# at some time in the future.
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
