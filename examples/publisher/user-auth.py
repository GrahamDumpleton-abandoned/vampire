# This file exhibits how authentication can be used.
#
# Note that an auth realm is mandatory when using
# Vampire. In mod_python.publisher it defaults to
# "unknown" if not set which is different to what Apache
# allows. In Vampire if an auth realm is not set a 500
# error is returned.

__auth_realm__ = "Disney Land"
__auth__ = { "mickey": "mouse", "minney": "mouse", "donald": "duck" }

# Any of the above can access method1().

def method1():
  return "method1"

# Only "mickey" can access "method2()".

def method2():
  def __access__(req,user):
    return user == "mickey"
  return "method2"

class Object1:

  __access__ = [ "minney", "donald" ]

  # Both "minney" and "donald" can access "method3()".

  def method3(self):
    return "method3"

  # Only "minney" can access "method4()".
  #
  # Note that mod_python.publisher doesn't support
  # authentication within methods of a class. Vampire
  # fixes this and thus why "__access__" in this context
  # does actually restrict access to just "minney".

  def method4(self):
    def __access__(req,user):
      return user == "minney"
    return "method4"

object1 = Object1()

# Note that in mod_python.publisher different sets of
# authentication credentials cannot not be nested within
# each other in certain ways as it causes browsers to go
# into loops. Vampire however fixes this bug in
# mod_python.publisher.

class Object2:

  __auth_realm__ = "Top Secret"
  __auth__ = { "donald": "duck" }
  __access__ = [ "donald" ]

  # Only "donald" can access "method5()".

  def method5(self):
    return "method5"

object2 = Object2()
