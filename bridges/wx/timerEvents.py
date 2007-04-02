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

from TG.helix.events.timerEvents import TimerEventSource, IdleEventSource
from .common import wx, wxEventSourceMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxTimerEventSource(wxEventSourceMixin, TimerEventSource):
    def __init__(self, glCanvas, stage):
        frequency = getattr(stage, 'timerFrequency', 60.)
        TimerEventSource.__init__(self)
        wxEventSourceMixin.__init__(self, glCanvas)
        self._timer = wx.Timer()
        if getattr(stage, 'exitOnError', True):
            self._timer.Bind(wx.EVT_TIMER, self.onEvtTimer_exitError)
        else:
            self._timer.Bind(wx.EVT_TIMER, self.onEvtTimer)
        self._timer.Start(int(1000/frequency), False)

    _frequency = None
    def getFrequency(self):
        return 1000./self._timer.GetInterval()
    def setFrequency(self, frequency):
        self._timer.Start(int(1000/frequency), False)
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

    def onEvtTimer_exitError(self, evt):
        if not self:
            self._timer.Stop()
            del self._timer
            return

        info = self.newInfo()
        info.update(self._globalMouseInfo())

        try:
            if not self.sendTimer(info):
                evt.Skip()
        except Exception, err:
            self.exitOnError(err)

    def exitOnError(self, err):
        traceback.print_exc()
        wx.GetApp().Exit()
        sys.exit(-1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxIdleEventSource(wxEventSourceMixin, IdleEventSource):
    def __init__(self, glCanvas, stage):
        IdleEventSource.__init__(self)
        wxEventSourceMixin.__init__(self, glCanvas)
        glCanvas.Bind(wx.EVT_IDLE, self.onEvtIdle)

    def onEvtIdle(self, evt):
        info = self.newInfo()
        info.update(self._globalMouseInfo())
        if not self.sendIdle(info):
            evt.Skip()
        else: evt.RequestMore()

