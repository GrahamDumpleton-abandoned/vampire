#!/usr/bin/env python


"""
Autogenerated by CHEETAH: The Python-Powered Template Engine
 CHEETAH VERSION: 0.9.16b1
 Generation time: Sun Jun  5 21:44:38 2005
   Source file: index.tmpl
   Source file last modified: Sun Jun  5 21:44:34 2005
"""

__CHEETAH_genTime__ = 'Sun Jun  5 21:44:38 2005'
__CHEETAH_src__ = 'index.tmpl'
__CHEETAH_version__ = '0.9.16b1'

##################################################
## DEPENDENCIES

import sys
import os
import os.path
from os.path import getmtime, exists
import time
import types
import __builtin__
from Cheetah.Template import Template
from Cheetah.DummyTransaction import DummyTransaction
from Cheetah.NameMapper import NotFound, valueForName, valueFromFrameOrSearchList
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers
from _layout import _layout
import vampire

##################################################
## MODULE CONSTANTS

try:
    True, False
except NameError:
    True, False = (1==1), (1==0)
VFFSL=valueFromFrameOrSearchList
VFN=valueForName
currentTime=time.time

##################################################
## CLASSES

class index(_layout):
    """
    
    Autogenerated by CHEETAH: The Python-Powered Template Engine
    """

    ##################################################
    ## GENERATED METHODS


    def __init__(self, *args, **KWs):
        """
        
        """

        _layout.__init__(self, *args, **KWs)

    def title(self,
            trans=None,
            dummyTrans=False,
            VFFSL=valueFromFrameOrSearchList,
            VFN=valueForName,
            getmtime=getmtime,
            currentTime=time.time):


        """
        Generated from #def title at line 4, col 1.
        """

        if not trans:
            trans = DummyTransaction()
            dummyTrans = True
        write = trans.response().write
        SL = self._searchList
        filter = self._currentFilter
        globalSetVars = self._globalSetVars
        
        ########################################
        ## START - generated method body
        
        write('Home Page')
        
        ########################################
        ## END - generated method body
        
        if dummyTrans:
            return trans.response().getvalue()
        else:
            return ""
        

    def body(self,
            trans=None,
            dummyTrans=False,
            VFFSL=valueFromFrameOrSearchList,
            VFN=valueForName,
            getmtime=getmtime,
            currentTime=time.time):


        """
        This is the main method generated by Cheetah
        """

        if not trans:
            trans = DummyTransaction()
            dummyTrans = True
        write = trans.response().write
        SL = self._searchList
        filter = self._currentFilter
        globalSetVars = self._globalSetVars
        
        ########################################
        ## START - generated method body
        
        write('\n\n')
        config = VFN(VFFSL(SL,"vampire",True),"loadConfig",False)(VFFSL(SL,"req",True),".vampire")
        user_logout = VFN(VFFSL(SL,"config",True),"get",False)("Access","user_logout")
        write('\n<p>\nHello ')
        write(filter(VFN(VFFSL(SL,"req",True),"session",True)["profile"]["fullname"], rawExpr='$req.session["profile"]["fullname"]')) # from line 13, col 7.
        write('''.
</p>
<p>
Would you like to look at your user <a href="profile.html">profile</a>?
</p>

<p>
Or perhaps you want to <a href="''')
        write(filter(VFFSL(SL,"user_logout",True), rawExpr='$user_logout')) # from line 20, col 33.
        write('''">logout</a> instead?
</p>

<p>
Note that this index page, the login form and the user profile page are all
implemented using Cheetah.
</p>
<p>
You should also check out the sample pages implemented using a
<a href="sample_1.html">handler</a>, <a href="sample_2.html">PSP</a>
and <a href="sample_3.html">HTMLTemplate</a>.
</p>
<p>
Note how you can't actually tell how they are implemented, since the
URL always uses a ".html" extension.
</p>
''')
        
        ########################################
        ## END - generated method body
        
        if dummyTrans:
            return trans.response().getvalue()
        else:
            return ""
        
    ##################################################
    ## GENERATED ATTRIBUTES


    _mainCheetahMethod_for_index= 'body'


# CHEETAH was developed by Tavis Rudd, Mike Orr, Ian Bicking and Chuck Esterbrook;
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org

##################################################
## if run from command line:
if __name__ == '__main__':
    index().runAsMainProgram()

