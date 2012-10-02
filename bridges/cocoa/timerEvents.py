# -*- coding: utf-8 -*- vim: set ts=4 sw=4 expandtab
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2012  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

import sys
import Cocoa, objc
from Cocoa import NSTimer
from .common import CocoaEventSourceMixin

class CocoaTimerEventSource(CocoaEventSourceMixin):
    channelKey = 'timer'

    def bindHost(self, glview, options):
        freq = options.get('timerFrequency', 60.)
        self.setFrequency(freq)

    _timer = None
    def getFrequency(self):
        if self._timer is not None:
            return 1000./self._timer.GetInterval()
    def setFrequency(self, frequency):
        if self._timer is not None:
            self._timer.invalidate()
            self._timer = None
        self._timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                1./frequency, self, 'onEvtTimer', None, True)
    frequency = property(getFrequency, setFrequency)

    def onEvtTimer(self):
        try:
            if not self:
                self._timer.invalidate()
                del self._timer
                return

            info = self.newInfo(etype='animate', ekind='timer')
            if not self.addKeyMouseInfo(info):
                return

            self.evtRoot.send(self.channelKey, info)
        except Exception:
            sys.excepthook(*sys.exc_info())

