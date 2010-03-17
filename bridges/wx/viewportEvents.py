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
from .common import wx, wxEventSourceMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxViewportEventSource(wxEventSourceMixin):
    channelKey = 'viewport'
    def bindHost(self, glCanvas, options):
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
        info = self.newInfo(viewSize=tuple(evt.GetSize()))
        if not self.addKeyMouseInfo(info):
            evt.Skip()
            return
        self.evtRoot.send(self.channelKey + '-size', info)
        if info.get('skip', True):
            evt.Skip()

    def onEvtEraseBackground(self, evt):
        evt.Skip()

    def onEvtPaint(self, evt):
        wx.PaintDC(evt.GetEventObject())
        info = self.newInfo(viewSize=tuple(self.glCanvas.GetSize()))
        if not self.addKeyMouseInfo(info):
            evt.Skip()
            return
        self.evtRoot.send(self.channelKey + '-paint', info)
        if info.get('skip', True):
            evt.Skip()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onEvtSize_exitError(self, evt):
        try: self.onEvtSize(evt)
        except Exception, err:
            self.exitOnError(err)

    def onEvtEraseBackground_exitError(self, evt):
        try: self.onEvtEraseBackground(evt)
        except Exception, err:
            self.exitOnError(err)

    def onEvtPaint_exitError(self, evt):
        try: self.onEvtPaint(evt)
        except Exception, err:
            self.exitOnError(err)

    def exitOnError(self, err):
        sys.excepthook(*sys.exc_info())
        wx.GetApp().Exit()
        sys.exit(-1)

