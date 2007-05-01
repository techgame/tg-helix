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

from TG.helix.actors.events import HostViewEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxEventSourceMixin(HostViewEventSource):
    channelKey = None

    def __init__(self, glCanvas, options):
        self.options = options
        self.glCanvas = glCanvas

    def evtRootSetup(self, evtRoot):
        self.evtRoot = evtRoot
        channels = evtRoot.getChannels()

        if self.channelKey is not None:
            self.channel = channels[self.channelKey]
        else: self.channels = channels

        self.bindHost(self.glCanvas, self.options)

    def __nonzero__(self):
        return bool(self.glCanvas)

    def bindHost(self, glCanvas, options):
        pass

    def getViewSize(self):
        return tuple(self.glCanvas.GetClientSize())
    def setViewCurrent(self):
        return self.glCanvas.SetCurrent()
    def viewSwapBuffers(self):
        return self.glCanvas.SwapBuffers()

    def getKeyMouseInfo(self, pos=None, evt=None):
        wxhost = self.glCanvas
        eoHeight = wxhost.GetClientSize()[1]

        if pos is None:
            pos = tuple(wxhost.ScreenToClient(wx.GetMousePosition()))
        pos = (pos[0], eoHeight - pos[1])

        mouseState = wx.GetMouseState()

        if evt is None:
            evt = mouseState

        # mouseState is more accurate for combinations of buttons
        modifiers = [evt.AltDown() and 'alt', evt.ControlDown() and 'control', evt.ShiftDown() and 'shift', evt.MetaDown() and 'meta']
        modifiers = set(filter(None, modifiers))

        buttons = [mouseState.LeftDown() and 'left', mouseState.RightDown() and 'right', mouseState.MiddleDown() and 'middle']
        buttons = set(filter(None, buttons))

        info = dict(pos=pos, buttons=buttons, modifiers=modifiers)
        return info

