#!/usr/bin/env python


"""
Autogenerated by CHEETAH: The Python-Powered Template Engine
 CHEETAH VERSION: 0.9.16b1
 Generation time: Mon May 16 21:42:59 2005
   Source file: python_config.tmpl
   Source file last modified: Mon May 16 21:41:49 2005
"""

__CHEETAH_genTime__ = 'Mon May 16 21:42:59 2005'
__CHEETAH_src__ = 'python_config.tmpl'
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

class python_config(_layout):
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
        
        write('Python Config')
        
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
        config = VFN(VFFSL(SL,"req",True),"get_config",False)()
        keys = VFN(VFFSL(SL,"config",True),"keys",False)()
        VFN(VFFSL(SL,"keys",True),"sort",False)()
        write('''
<p>
<table>

<thead>
<tr>
<th>Key</th>
<th>Value</th>
</tr>
</thead>

<tbody>
''')
        for key in VFFSL(SL,"keys",True):
            write('    <tr>\n    <td>')
            write(filter(VFFSL(SL,"key",True), rawExpr='$key')) # from line 25, col 9.
            write('</td>\n    <td>')
            write(filter(VFFSL(SL,"config",True)[VFFSL(SL,"key",True)], rawExpr='$config[$key]')) # from line 26, col 9.
            write('</td>\n    </tr>\n')
        write('''</tbody>

</table>
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


    _mainCheetahMethod_for_python_config= 'body'


# CHEETAH was developed by Tavis Rudd, Mike Orr, Ian Bicking and Chuck Esterbrook;
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org

##################################################
## if run from command line:
if __name__ == '__main__':
    python_config().runAsMainProgram()

