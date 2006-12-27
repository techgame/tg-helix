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
from TG.helix.events.timerEvents import GLTimerEventSource, GLIdleEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxGLTimerEventSource(wxEventSourceMixin, GLTimerEventSource):
    def __init__(self, glCanvas, frequency=60.):
        GLTimerEventSource.__init__(self)
        wxEventSourceMixin.__init__(self, glCanvas)
        self._timer = wx.Timer()
        self._timer.Bind(wx.EVT_TIMER, self.onEvtTimer)
        self._timer.Start(1000//frequency, False)

    _frequency = None
    def getFrequency(self):
        return 1000./self._timer.GetInterval()
    def setFrequency(self, frequency):
        self._timer.Start(1000//frequency, False)
    frequency = property(getFrequency, setFrequency)

    def onEvtTimer(self, evt):
        if not self:
            self._timer.Stop()
            del self._timer
            return

        info = self.newInfo()
        info.update(self._globalMouseInfo())
        if not self.sendTimer(info):
            evt.Skip()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxGLIdleEventSource(wxEventSourceMixin, GLIdleEventSource):
    def __init__(self, glCanvas, frequency=60.):
        GLIdleEventSource.__init__(self)
        wxEventSourceMixin.__init__(self, glCanvas)
        glCanvas.Bind(wx.EVT_IDLE, self.onEvtIdle)

    def onEvtIdle(self, evt):
        info = self.newInfo()
        info.update(self._globalMouseInfo())
        if not self.sendIdle(info):
            evt.Skip()
        else: evt.RequestMore()

