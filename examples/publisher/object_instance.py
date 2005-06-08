import vampire
import time

class Old:

  def __init__(self):
    self.__time = time.time()

  def __call__(self,req,arg1=None,arg2=None):
    return self.__time,"Old.__call__()",arg1,arg2

old = vampire.Instance(Old)

class New(object):

  def __init__(self):
    self.__time = time.time()

  def __call__(self,req,arg1=None,arg2=None):
    return self.__time,"New.__call__()",arg1,arg2

new = vampire.Instance(New)
