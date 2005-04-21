#!/usr/bin/env python


"""
Autogenerated by CHEETAH: The Python-Powered Template Engine
 CHEETAH VERSION: 0.9.16b1
 Generation time: Thu Apr 21 13:07:42 2005
   Source file: index.tmpl
   Source file last modified: Thu Apr 21 13:07:38 2005
"""

__CHEETAH_genTime__ = 'Thu Apr 21 13:07:42 2005'
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
        
        write('Index Page\n')
        
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
        defaults = VFFSL(SL,"req.config.defaults",True)
        baseurl = VFFSL(SL,"defaults",True)["__baseurl_rel__"]
        write('''
<h2>Form Values</h2>

<p><a href="''')
        write(filter(VFFSL(SL,"baseurl",True), rawExpr='$baseurl')) # from line 13, col 13.
        write('/fields.html">Test Script</a></p>\n\n<p><a href="')
        write(filter(VFFSL(SL,"baseurl",True), rawExpr='$baseurl')) # from line 15, col 13.
        write('/fields.html?a=b">a=b</a></p>\n<p><a href="')
        write(filter(VFFSL(SL,"baseurl",True), rawExpr='$baseurl')) # from line 16, col 13.
        write('/fields.html?a=b&c=d">a=b&c=d</a></p>\n<p><a href="')
        write(filter(VFFSL(SL,"baseurl",True), rawExpr='$baseurl')) # from line 17, col 13.
        write('/fields.html?a.b=c&a.b=d">a.b=c&a.b=d</a></p>\n<p><a href="')
        write(filter(VFFSL(SL,"baseurl",True), rawExpr='$baseurl')) # from line 18, col 13.
        write('/fields.html?a-1=b&a-2=c">a-1=b&a-2=c</a></p>\n<p><a href="')
        write(filter(VFFSL(SL,"baseurl",True), rawExpr='$baseurl')) # from line 19, col 13.
        write('/fields.html?a.b-1=c&a.b-2=d">a.b-1=c&a.b-2=d</a></p>\n<p><a href="')
        write(filter(VFFSL(SL,"baseurl",True), rawExpr='$baseurl')) # from line 20, col 13.
        write('''/fields.html?a-1.c=d&a-2.e=f">a-1.c=d&a-2.e=f</a></p>

<h2>Vampire Config</h2>

<p><a href="''')
        write(filter(VFFSL(SL,"baseurl",True), rawExpr='$baseurl')) # from line 24, col 13.
        write('/defaults.html">Config Defaults</a></p>\n<p><a href="')
        write(filter(VFFSL(SL,"baseurl",True), rawExpr='$baseurl')) # from line 25, col 13.
        write('/config.html">Config Values</a></p>\n<p><a href="')
        write(filter(VFFSL(SL,"baseurl",True), rawExpr='$baseurl')) # from line 26, col 13.
        write('/config.html?raw=1">Raw Settings</a></p>\n')
        
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

