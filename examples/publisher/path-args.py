import vampire

# The "vampire.PathArgs()" class can be used to wrap a
# method so that any additional path information beyond
# that which was required to match the original method
# will be accumulated and each component of the past
# passed in to the method as a distinct parameter.
# Because each component of the path information is
# passed as a separate parameter, there can only be as
# much additional path information as the parameters
# allow. Note that any form parameters will be ignored,
# but if the first parameter is called "req" it will
# still be passed the request object. Default parameters
# can be specified as can a varargs parameter. There is
# no equivalent functionality in mod_python.publisher
# for this feature.

def _method1(year,month,day="0"):
  return "_method1",year,month,day

# URL: "/method1/1/2".
# Result: year="1", month="2", day="0".

# URL: "/method1/1/2/3".
# Result: year="1", month="2", day="3".

method1 = vampire.PathArgs(_method1)

def _method2(req,year,month,day="0"):
  return "_method2",year,month,day

# URL: "/method2/1/2".
# Result: year="1", month="2", day="0".

# URL: "/method2/1/2/3".
# Result: year="1", month="2", day="3".

method2 = vampire.PathArgs(_method2)

def _method3(req,year,mon,day="0",*va):
  return "_method3",year,mon,day,va

# URL: "/method3/1/2".
# Result: year="1", month="2", day="0", args=()

# URL: "/method3/1/2/3".
# Result: year="1", month="2", day="3", args=()

# URL: "/method3/1/2/3/4".
# Result: year="1", month="2", day="3", args=("4",)

# URL: "/method3/1/2/3/4/5".
# Result: year="1", month="2", day="3", args=("4","5")

method3 = vampire.PathArgs(_method3)
