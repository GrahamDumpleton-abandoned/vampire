# This file exhibits how user authentication can be used.

__auth_realm__ = "Top Secret"
__auth__ = { "mickey": "mouse", "minney": "mouse", "donald": "duck" }

# Any of the above can access method1().

def method1():
  return "method1"

# Only "mickey" can access "method2()".

def method2():
  def __access__(req,user):
    return user == "mickey"
  return "method2"

# Both "minney" and "donald" can access "object1".
# Both "minney" and "donald" can access "object1.method3()".
# Both "minney" and "donald" can access "object1.method4()".
#
# This should not be the case for "object1.method4()"
# and access should only be available to "minney", but
# as of mod_python 3.1.4 it doesn't support methods for
# authentication within MethodType and Vampire uses the
# authentication routine from mod_python rather than
# using its own as this stage.

class Object1:

  __access__ = [ "minney", "donald" ]

  def method3(self):
    return "method3"

  def method4(self):
    def __access__(req,user):
      # This doesn't work here.
      return user == "minney"
    return "method4"

object1 = Object1()
