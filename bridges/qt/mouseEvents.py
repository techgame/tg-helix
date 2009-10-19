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

from .common import QtCore, QtGui, QE, qtEventSourceMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtMouseEventSource(qtEventSourceMixin):
    channelKey = 'mouse'

    def bindHost(self, glCanvas, options):
        glCanvas.setMouseTracking(True)
        glCanvas.bindEvent(QtGui.QMouseEvent, self.onEvtMouse)
        glCanvas.bindEvent(QtGui.QHoverEvent, self.onEvtHover)
        glCanvas.bindEvent(QtGui.QWheelEvent, self.onEvtMouseWheel)

    def onEvtMouse(self, evt):
        etype, ekind = self.qtEtypeMap[evt.type()]

        info = self.newInfo(etype=etype, ekind=ekind)

        if not self.addKeyMouseInfo(info, (evt.x(), evt.y()), evt):
            return False

        btn = self.qtButtonMap[evt.button()]
        if btn:
            info.update(btn=btn, op=btn+'-'+ekind)

        self.evtRoot.send(self.channelKey, info)
        self.checkCapture(info)

        if not info.get('skip', False):
            evt.accept()
            return True

    def onEvtMouseWheel(self, evt):
        etype, ekind = self.qtEtypeMap[evt.type()]
        info = self.newInfo(etype=etype, ekind=ekind)

        if not self.addKeyMouseInfo(info, (evt.x(), evt.y()), evt):
            return False

        info.update(
            wheel=evt.delta(),
            wheelLinesPer=evt.GetLinesPerAction(),
            wheelIsPage=evt.IsPageScroll())

        self.evtRoot.send(self.channelKey, info)
        self.checkCapture(info)
        if not info.get('skip', False):
            evt.accept()
            return True

    def onEvtHover(self, evt):
        try:
            etype, ekind = self.qtEtypeMap[evt.type()]
        except LookupError: 
            return False

        info = self.newInfo(etype=etype, ekind=ekind)

        if not self.addKeyMouseInfo(info, (evt.pos.x(), evt.pos.y()), evt):
            return False

        self.evtRoot.send(self.channelKey, info)
        self.checkCapture(info)
        if not info.get('skip', False):
            evt.accept()
            return True


    _captureState = False
    def checkCapture(self, info):
        capture = bool(info.get('capture', info.buttons))

        if capture != self._captureState:
            self._captureState = capture
            if capture:
                self.glCanvas.grabMouse()
                self.glCanvas.grabKeyboard()
            else: 
                self.glCanvas.releaseMouse()
                self.glCanvas.releaseKeyboard()

            self.onMouseCaptured(capture)

        return capture

    def onMouseCaptured(self, captured):
        ekind = ('acquire' if captured else 'release')
        info = self.newInfo(etype='capture', ekind=ekind, captured=captured)

        if self.addKeyMouseInfo(info):
            return False

        self.evtRoot.send(self.channelKey, info)
        return not info.get('skip', True)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    qtEtypeMap = {
        QE.MouseButtonDblClick: ('button', 'dclick'),
        QE.MouseButtonPress: ('button', 'down'),
        QE.MouseButtonRelease: ('button', 'up'),

        QE.MouseMove: ('motion', 'pos'),
        QE.Wheel: ('motion', 'wheel'),
        QE.MouseTrackingChange: ('motion', 'tracking'),
        
        QE.HoverEnter: ('window', 'enter'),
        QE.HoverLeave: ('window', 'leave'),
    }

