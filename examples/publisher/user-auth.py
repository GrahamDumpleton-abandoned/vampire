# Both Mickey and Donald can access this module.

__auth_realm__ = "Top Secret"
__auth__ = { "mickey": "mouse", "donald": "duck" }
__access__ = [ "mickey", "donald" ]

# Anyone with access to the module can access method1().

def method1():
  return "method1"

# Only Mickey can access method2().

def method2():

  def __access__(req,user):
    return user == "mickey"

  return "method2"
