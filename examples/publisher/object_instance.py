import vampire
import time

class OldStyleClass:

  def __init__(self):
    self.__time = time.time()

  def __call__(self,req,arg1=None,arg2=None):
    return self.__time,"OldStyleClass.__call__()",arg1,arg2

old_instance = vampire.Instance(OldStyleClass)

class NewStyleClass(object):

  def __init__(self):
    self.__time = time.time()

  def __call__(self,req,arg1=None,arg2=None):
    return self.__time,"NewStyleClass.__call__()",arg1,arg2

new_instance = vampire.Instance(NewStyleClass)
