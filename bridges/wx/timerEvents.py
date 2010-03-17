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

class wxTimerEventSource(wxEventSourceMixin):
    channelKey = 'timer'

    def bindHost(self, glCanvas, options):
        frequency = options.get('timerFrequency', 60.)
        self._timer = wx.Timer()

        if options.get('exitOnError', True):
            self._timer.Bind(wx.EVT_TIMER, self.onEvtTimer_exitError)
        else: self._timer.Bind(wx.EVT_TIMER, self.onEvtTimer)

        self._timer.Start(int(1000/frequency), False)

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

        info = self.newInfo(etype='animate', ekind='timer')
        if not self.addKeyMouseInfo(info):
            evt.Skip()
            return

        self.evtRoot.send(self.channelKey, info)

    def onEvtTimer_exitError(self, evt):
        try: self.onEvtTimer(evt)
        except Exception, err:
            self.exitOnError(err)

    def exitOnError(self, err):
        sys.excepthook(*sys.exc_info())
        wx.GetApp().Exit()
        sys.exit(-1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxIdleEventSource(wxEventSourceMixin):
    channelKey = 'idle'

    def bindHost(self, glCanvas, options):
        if options.get('exitOnError', True):
            glCanvas.Bind(wx.EVT_IDLE, self.onEvtIdle_exitError)
        else: glCanvas.Bind(wx.EVT_IDLE, self.onEvtIdle)

    def onEvtIdle(self, evt):
        info = self.newInfo(etype='idle', ekind='idle')
        if not self.addKeyMouseInfo(info):
            evt.Skip()
            return
        self.evtRoot.send(self.channelKey, info)

        if info.get('skip', True):
            evt.Skip()
        else: evt.RequestMore()

    def onEvtIdle_exitError(self, evt):
        try: self.onEvtIdle(evt)
        except Exception, err:
            self.exitOnError(err)

