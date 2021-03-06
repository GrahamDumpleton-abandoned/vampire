#!/usr/bin/env python


"""
Autogenerated by CHEETAH: The Python-Powered Template Engine
 CHEETAH VERSION: 0.9.16b1
 Generation time: Mon May 16 21:42:58 2005
   Source file: cached_templates.tmpl
   Source file last modified: Mon May 16 21:41:38 2005
"""

__CHEETAH_genTime__ = 'Mon May 16 21:42:58 2005'
__CHEETAH_src__ = 'cached_templates.tmpl'
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
import time

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

class cached_templates(_layout):
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
        
        write('Cached Templates')
        
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
        
        write('''


''')
        cache = VFN(VFFSL(SL,"vampire",True),"TemplateCache",False)()
        keys = VFN(VFFSL(SL,"cache",True),"cachedTemplates",False)()
        VFN(VFFSL(SL,"keys",True),"sort",False)()
        write('''
<p>
<table>

<thead>
<tr>
<th>Path</td>
<th>Node</td>
<th>Modified</td>
<th>Accessed</td>
<th>Hits</td>
</tr>
</thead>

<tbody>
''')
        for key in VFFSL(SL,"keys",True):
            info = VFN(VFFSL(SL,"cache",True),"templateInfo",False)(VFFSL(SL,"key",True))
            write('    <tr>\n    <td>')
            write(filter(VFFSL(SL,"info.path",True), rawExpr='$info.path')) # from line 32, col 9.
            write('</td>\n    <td>')
            write(filter(VFFSL(SL,"info.attribute",True), rawExpr='$info.attribute')) # from line 33, col 9.
            write('</td>\n    <td>')
            write(filter(VFN(VFFSL(SL,"time",True),"asctime",False)(VFN(VFFSL(SL,"time",True),"localtime",False)(VFFSL(SL,"info.mtime",True))), rawExpr='$time.asctime($time.localtime($info.mtime))')) # from line 34, col 9.
            write('</td>\n    <td>')
            write(filter(VFN(VFFSL(SL,"time",True),"asctime",False)(VFN(VFFSL(SL,"time",True),"localtime",False)(VFFSL(SL,"info.atime",True))), rawExpr='$time.asctime($time.localtime($info.atime))')) # from line 35, col 9.
            write('</td>\n    <td>')
            write(filter(VFFSL(SL,"info.hits",True), rawExpr='$info.hits')) # from line 36, col 9.
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


    _mainCheetahMethod_for_cached_templates= 'body'


# CHEETAH was developed by Tavis Rudd, Mike Orr, Ian Bicking and Chuck Esterbrook;
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org

##################################################
## if run from command line:
if __name__ == '__main__':
    cached_templates().runAsMainProgram()

