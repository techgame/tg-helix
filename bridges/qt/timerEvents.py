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

from .common import QtCore, qtEventSourceMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtTimerEventSource(qtEventSourceMixin):
    channelKey = 'timer'

    def bindHost(self, glCanvas, options):
        glCanvas.bindEvent(QtCore.QTimerEvent, self.onEvtTimer)
        self.frequency = options.get('timerFrequency', 60.)

    _frequency = 60
    def getFrequency(self):
        return self._frequency
    def setFrequency(self, frequency):
        self._frequency = float(frequency)
        self._startTimer()
    frequency = property(getFrequency, setFrequency)

    _timerId = None
    def _stopTimer(self):
        if self._timerId is not None:
            self.glCanvas.killTimer(self._timerId)
            self._timerId = None
            return True
        else:
            return False
    def _startTimer(self):
        self._stopTimer()
        msec = int(1000/self.frequency)
        self._timerId = self.glCanvas.startTimer(msec)
        return True

    def onEvtTimer(self, evt):
        if evt.timerId() != self._timerId:
            return False

        info = self.newInfo(etype='animate', ekind='timer')
        if self.addKeyMouseInfo(info):
            self.evtRoot.send(self.channelKey, info)

        evt.accept()
        return True

