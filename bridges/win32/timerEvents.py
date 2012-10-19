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

import sys, itertools
from .common import Win32EventSourceMixin
import ctypes
from ctypes import wintypes
from venster import windows

TIMERPROC = ctypes.WINFUNCTYPE(None, wintypes.HWND, wintypes.UINT, wintypes.UINT, wintypes.DWORD)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Win32TimerEventSource(Win32EventSourceMixin):
    channelKey = 'timer'

    def bindHost(self, glwin, options):
        glwin.bindEvt(windows.WM_CLOSE, self._onClose)
        self._timer = Win32Timer(glwin,
            frequency=options.get('timerFrequency', 60.)
            ).bindEx(self.onEvtTimer)

    def onEvtTimer(self, hwnd, umsg, timer, ts):
        info = self.newInfo(etype='animate', ekind='timer')
        if not self.addKeyMouseInfo(info): return

        self.evtRoot.send(self.channelKey, info)

    def _onClose(self, tgt, evt):
        evt.handled = False
        self._timer.unbind()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

nextTimerId = itertools.count(1000).next

class Win32Timer(object):
    def __init__(self, hwnd, **kw):
        self.hwnd = getattr(hwnd, 'handle', hwnd)
        v = kw.pop('interval', None)
        if v is not None:
            self.setInterval(v)
        v = kw.pop('frequency', None)
        if v is not None:
            self.setFrequency(v)

    def __del__(self):
        self.unbind()

    def unbind(self):
        htimer = self.handle
        if htimer:
            del self.handle
            windows.KillTimer(self.hwnd, htimer)
            return True
        else: return False

    _ms_interval = 100
    def getInterval(self):
        ms = self._ms_interval
        if ms is not None:
            return ms/1000.
    def setInterval(self, seconds):
        self._ms_interval = int(seconds/1000)
        return self._update()
    interval = property(getInterval, setInterval)

    def getFrequency(self):
        return 1./(self.getInterval() or 0.001)
    def setFrequency(self, frequency):
        return self.setInterval(1./(frequency or 0.001))
    frequency = property(getFrequency, setFrequency)

    _timerFn = None
    def bind(self, onTimer):
        return self.bindEx(lambda hwnd,umsg,timer,ts: onTimer())
    def bindEx(self, onTimerEvt):
        self._timerFn = TIMERPROC(onTimerEvt)
        return self._update()
    
    handle = None
    def __nonzero__(self):
        return bool(self.handle)
    def _update(self):
        if self._timerFn is not None:
            self.handle = windows.SetTimer(self.hwnd, self.handle or nextTimerId(), self._ms_interval, self._timerFn)
        return self

