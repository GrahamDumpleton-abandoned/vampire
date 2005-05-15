#!/usr/bin/env python


"""
Autogenerated by CHEETAH: The Python-Powered Template Engine
 CHEETAH VERSION: 0.9.16b1
 Generation time: Sun May 15 19:59:47 2005
   Source file: vampire_config.tmpl
   Source file last modified: Sun May 15 19:59:34 2005
"""

__CHEETAH_genTime__ = 'Sun May 15 19:59:47 2005'
__CHEETAH_src__ = 'vampire_config.tmpl'
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

class vampire_config(_layout):
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
        
        write('Vampire Config')
        
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
        options = VFN(VFFSL(SL,"req",True),"get_options",False)()
        keys = VFN(VFFSL(SL,"options",True),"keys",False)()
        VFN(VFFSL(SL,"keys",True),"sort",False)()
        write('''
<p>
<h2>.htaccess</h2>
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
            write('  <tr>\n    <td>')
            write(filter(VFFSL(SL,"key",True), rawExpr='$key')) # from line 26, col 9.
            write('</td>\n    <td>')
            write(filter(VFFSL(SL,"options",True)[VFFSL(SL,"key",True)], rawExpr='$options[$key]')) # from line 27, col 9.
            write('</td>\n  </tr>\n')
        write('''</tbody>

</table>
</p>

''')
        file = VFN(VFFSL(SL,"req.fields",True),"get",False)("file",".vampire")
        write('\n\n')
        config = VFN(VFFSL(SL,"vampire",True),"loadConfig",False)(VFFSL(SL,"req",True),VFFSL(SL,"file",True))
        defaults = VFN(VFFSL(SL,"config",True),"defaults",False)()
        write('\n')
        keys = VFN(VFFSL(SL,"defaults",True),"keys",False)()
        VFN(VFFSL(SL,"keys",True),"sort",False)()
        write('''
<p>
<h2>.vampire</h2>
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
            write('  <tr>\n    <td>')
            write(filter(VFFSL(SL,"key",True), rawExpr='$key')) # from line 59, col 9.
            write('</td>\n    <td>')
            write(filter(VFFSL(SL,"defaults",True)[VFFSL(SL,"key",True)], rawExpr='$defaults[$key]')) # from line 60, col 9.
            write('</td>\n  </tr>\n')
        write('''</tbody>

</table>
</p>

''')
        sections = VFN(VFFSL(SL,"config",True),"sections",False)()
        VFN(VFFSL(SL,"sections",True),"sort",False)()
        write('\n')
        for section in VFFSL(SL,"sections",True):
            write('<p vampire:node="rep:section">\n<h3>')
            write(filter(VFFSL(SL,"section",True), rawExpr='$section')) # from line 73, col 5.
            write('''</h3>
<table>

<thead>
  <tr>
    <td><strong>Key</strong></td>
    <td><strong>Value</strong></td>
  </tr>
</thead>

<tbody>
''')
            keys = VFN(VFFSL(SL,"config",True),"options",False)(VFFSL(SL,"section",True))
            VFN(VFFSL(SL,"keys",True),"sort",False)()
            for key in VFFSL(SL,"keys",True):
                write('  <tr>\n    <td>')
                write(filter(VFFSL(SL,"key",True), rawExpr='$key')) # from line 88, col 9.
                write('</td>\n    <td>')
                write(filter(VFN(VFFSL(SL,"config",True),"get",False)(VFFSL(SL,"section",True),VFFSL(SL,"key",True)), rawExpr='$config.get($section,$key)')) # from line 89, col 9.
                write('</td>\n  </tr>\n')
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


    _mainCheetahMethod_for_vampire_config= 'body'


# CHEETAH was developed by Tavis Rudd, Mike Orr, Ian Bicking and Chuck Esterbrook;
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org

##################################################
## if run from command line:
if __name__ == '__main__':
    vampire_config().runAsMainProgram()

