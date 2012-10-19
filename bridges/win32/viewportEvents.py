##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

import sys
import ctypes
from .common import Win32EventSourceMixin
from venster import windows

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PaintStruct(ctypes.Structure):
    _fields_ = [('opaque', ctypes.c_void_p*32)]

class Win32ViewportEventSource(Win32EventSourceMixin):
    channelKey = 'viewport'
    def bindHost(self, glwin, options):
        glwin.bindEvt(windows.WM_SIZE, self.onEvtSize)
        glwin.bindEvt(windows.WM_ERASEBKGND, self.onEvtEraseBackground)
        glwin.bindEvt(windows.WM_PAINT, self.onEvtPaint)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onEvtSize(self, tgt, evt):
        info = self.newInfo()
        if not self.addKeyMouseInfo(info): return

        self.glwin.makeCurrentContext()
        self.evtRoot.send(self.channelKey + '-size', info)

    def onEvtEraseBackground(self, tgt, evt):
        evt.handled = True
        return 1

    def onEvtPaint(self, tgt, evt):
        evt.handled = True
        info = self.newInfo()
        if not self.addKeyMouseInfo(info): return

        win = self.glwin
        ps = PaintStruct()
        with win.inCurrentContext() as hdc:
            win.BeginPaint(ps)
            self.evtRoot.send(self.channelKey + '-paint', info)
            win.EndPaint(ps)

