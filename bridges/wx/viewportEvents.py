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
import traceback

from TG.helix.events.viewportEvents import ViewportEventSource
from .common import wx, wxEventSourceMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxViewportEventSource(wxEventSourceMixin, ViewportEventSource):
    def __init__(self, glCanvas, options):
        ViewportEventSource.__init__(self)
        wxEventSourceMixin.__init__(self, glCanvas)

        if options.get('exitOnError', True):
            glCanvas.Bind(wx.EVT_SIZE, self.onEvtSize_exitError)
            glCanvas.Bind(wx.EVT_ERASE_BACKGROUND, self.onEvtEraseBackground_exitError)
            glCanvas.Bind(wx.EVT_PAINT, self.onEvtPaint_exitError)
        else:
            glCanvas.Bind(wx.EVT_SIZE, self.onEvtSize)
            glCanvas.Bind(wx.EVT_ERASE_BACKGROUND, self.onEvtEraseBackground)
            glCanvas.Bind(wx.EVT_PAINT, self.onEvtPaint)

        glCanvas.SetCurrent()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onEvtSize(self, evt):
        if not self.sendSize(tuple(evt.GetSize())):
            evt.Skip()

    def onEvtEraseBackground(self, evt):
        if not self.sendErase():
            evt.Skip()

    def onEvtPaint(self, evt):
        wx.PaintDC(evt.GetEventObject())
        if not self.sendPaint():
            evt.Skip()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onEvtSize_exitError(self, evt):
        try:
            if not self.sendSize(tuple(evt.GetSize())):
                evt.Skip()
        except Exception, err:
            self.exitOnError(err)

    def onEvtEraseBackground_exitError(self, evt):
        try:
            if not self.sendErase():
                evt.Skip()
        except Exception, err:
            self.exitOnError(err)

    def onEvtPaint_exitError(self, evt):
        wx.PaintDC(evt.GetEventObject())
        try:
            if not self.sendPaint():
                evt.Skip()
        except Exception, err:
            self.exitOnError(err)

    def exitOnError(self, err):
        traceback.print_exc()
        wx.GetApp().Exit()
        sys.exit(-1)

