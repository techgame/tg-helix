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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxEventSourceMixin(object):
    modifierByBit = {
        0x1: 'alt',
        0x2: 'control',
        0x4: 'shift',
        0x8: 'meta',
        }

    def __init__(self, glCanvas):
        self.__glCanvas = glCanvas
        self.timingLog = []

    def __nonzero__(self):
        return bool(self.__glCanvas)

    def getViewSize(self):
        return tuple(self.__glCanvas.GetClientSize())
    def setViewCurrent(self):
        return self.__glCanvas.SetCurrent()
    def viewSwapBuffers(self):
        return self.__glCanvas.SwapBuffers()

    def _globalMouseInfo(self):
        wxhost = self.__glCanvas
        eoHeight = wxhost.GetClientSize()[1]
        mousePos = tuple(wxhost.ScreenToClient(wx.GetMousePosition()))
        mousePos = (mousePos[0], eoHeight - mousePos[1])
        mouseState = wx.GetMouseState()
        mouseButtons=((mouseState.LeftDown() and 0x1) | (mouseState.RightDown() and 0x2) | (mouseState.MiddleDown() and 0x4))
        return dict(pos=mousePos, buttons=mouseButtons)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if sys.platform.startswith('win'):
        timestamp = staticmethod(time.clock)
    else: 
        timestamp = staticmethod(time.time)

    def frameStart(self):
        self._tstart = self.timestamp()
    def frameEnd(self):
        tend = self.timestamp()
        self.fpsUpdate(self._tstart, tend)

    _lastUpdate = 0
    _historyKeep = 10
    _historyLen = 0
    fpsFormat = '%.1f fps (refresh), %.0f fps (render)'
    def fpsUpdate(self, renderStart, renderEnd):
        self.timingLog.append(renderEnd - renderStart)

        timeDelta = renderEnd - self._lastUpdate
        if timeDelta >= 1 and len(self.timingLog):
            newEntries = (len(self.timingLog) - self._historyLen - 1)
            fpsRefresh = newEntries / timeDelta
            fpsRender = len(self.timingLog) / sum(self.timingLog, 0.0)

            self._updateFPSInfo(fpsRefresh, fpsRender)

            self.timingLog = self.timingLog[-self._historyKeep:]
            self._historyLen = len(self.timingLog)
            self._lastUpdate = renderEnd
            return True

    def _updateFPSInfo(self, fpsRefresh, fpsRender):
        fpsStr = self.fpsFormat % (fpsRefresh, fpsRender)
        self._printFPS(fpsStr)

    fpsStr = 'Waiting'
    def _printFPS(self, fpsStr):
        self.fpsStr = fpsStr
        print '\r', fpsStr.ljust(75),
        sys.stdout.flush()

