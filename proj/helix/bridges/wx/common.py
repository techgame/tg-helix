##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys
import time

import wx

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxEventSourceMixin(object):
    modifierByBit = {
        0x1: 'alt',
        0x2: 'control',
        0x4: 'shift',
        0x8: 'meta',
        }

    def __init__(self, glCanvas):
        self.__glCanvas = glCanvas
        self.timingLog = []

    def __nonzero__(self):
        return bool(self.__glCanvas)

    def getViewSize(self):
        return tuple(self.__glCanvas.GetClientSize())
    def setViewCurrent(self):
        return self.__glCanvas.SetCurrent()
    def viewSwapBuffers(self):
        return self.__glCanvas.SwapBuffers()

    def _globalMouseInfo(self):
        wxhost = self.__glCanvas
        eoHeight = wxhost.GetClientSize()[1]
        mousePos = tuple(wxhost.ScreenToClient(wx.GetMousePosition()))
        mousePos = (mousePos[0], eoHeight - mousePos[1])
        mouseState = wx.GetMouseState()
        mouseButtons=((mouseState.LeftDown() and 0x1) | (mouseState.RightDown() and 0x2) | (mouseState.MiddleDown() and 0x4))
        return dict(pos=mousePos, buttons=mouseButtons)

