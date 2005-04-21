#!/usr/bin/env python


"""
Autogenerated by CHEETAH: The Python-Powered Template Engine
 CHEETAH VERSION: 0.9.16b1
 Generation time: Thu Apr 21 13:25:47 2005
   Source file: config.tmpl
   Source file last modified: Thu Apr 21 13:04:13 2005
"""

__CHEETAH_genTime__ = 'Thu Apr 21 13:25:47 2005'
__CHEETAH_src__ = 'config.tmpl'
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

class config(_layout):
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
        
        write('Vampire Config\n')
        
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
        config = VFFSL(SL,"req.config",True)
        sections = VFFSL(SL,"config.sections",True)
        VFN(VFFSL(SL,"sections",True),"sort",False)()
        raw = VFN(VFFSL(SL,"req.fields",True),"get",False)("raw",None)
        write('\n')
        for section in VFFSL(SL,"sections",True):
            write('<p>\n<h2>')
            write(filter(VFFSL(SL,"section",True), rawExpr='$section')) # from line 15, col 5.
            write('''</h2>
<table>
<thead>
<tr>
<td><strong>Key</strong></td>
<td><strong>Value</strong></td>
</tr>
</thead>
<tbody>
''')
            fields = VFN(VFFSL(SL,"config",True),"options",False)(VFFSL(SL,"section",True))
            VFN(VFFSL(SL,"fields",True),"sort",False)()
            for field in VFFSL(SL,"fields",True):
                write('<tr>\n<td>')
                write(filter(VFFSL(SL,"field",True), rawExpr='$field')) # from line 28, col 5.
                write('</td>\n<td>')
                write(filter(VFN(VFFSL(SL,"config",True),"get",False)(VFFSL(SL,"section",True),VFFSL(SL,"field",True),raw=VFFSL(SL,"raw",True)), rawExpr='$config.get($section,$field,raw=$raw)')) # from line 29, col 5.
                write('</td>\n</tr>\n')
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


    _mainCheetahMethod_for_config= 'body'


# CHEETAH was developed by Tavis Rudd, Mike Orr, Ian Bicking and Chuck Esterbrook;
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org

##################################################
## if run from command line:
if __name__ == '__main__':
    config().runAsMainProgram()

