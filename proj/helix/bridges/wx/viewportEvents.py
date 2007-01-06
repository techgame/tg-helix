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

from .common import wx, wxEventSourceMixin
from TG.helix.events.viewportEvents import ViewportEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxViewportEventSource(wxEventSourceMixin, ViewportEventSource):
    def __init__(self, glCanvas):
        ViewportEventSource.__init__(self)
        wxEventSourceMixin.__init__(self, glCanvas)
        glCanvas.Bind(wx.EVT_SIZE, self.onEvtSize)
        glCanvas.Bind(wx.EVT_ERASE_BACKGROUND, self.onEvtEraseBackground)
        glCanvas.Bind(wx.EVT_PAINT, self.onEvtPaint)
        glCanvas.SetCurrent()

    def onEvtSize(self, evt):
        if not self.sendSize(tuple(evt.GetSize())):
            evt.Skip()

    def onEvtEraseBackground(self, evt):
        if not self.sendErase():
            evt.Skip()

    def onEvtPaint(self, evt):
        if not self.sendPaint():
            evt.Skip()

