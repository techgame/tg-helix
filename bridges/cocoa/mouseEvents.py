# -*- coding: utf-8 -*- vim: set ts=4 sw=4 expandtab
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2012  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

import math
import Cocoa
from .common import CocoaEventSourceMixin

class CocoaMouseEventSource(CocoaEventSourceMixin):
    channelKey = 'mouse'

    def bindHost(self, glview, options):
        glview.window().setAcceptsMouseMovedEvents_(True)
        glview.events.bind('mouse', self.onEvtMouse)

    def onEvtMouse(self, evt, etype, ekind, btn=None):
        if etype=='button' and ekind=='down' and evt.clickCount()>1:
            ekind = 'dclick'
        info = self.newInfo(etype=etype, ekind=ekind)
        
        if btn:
            info.update(btn=btn, op=btn+'-'+ekind)

        if ekind == 'wheel':
            rotation = evt.scrollingDeltaY()
            info.update(wheel=rotation,
                wheelLinesPer=int(math.ceil(rotation)),
                wheelIsPage=False)

        pos = tuple(evt.locationInWindow())
        if not self.addKeyMouseInfo(info, pos, evt):
            return

        self.evtRoot.send(self.channelKey, info)
        self.checkCapture(info)

    _captureState = False
    def checkCapture(self, info):
        capture = bool(info.get('capture', info.buttons))
        if capture != self._captureState:
            self._captureState = capture
            self.onMouseCaptured(capture)
        return capture

    def onMouseCaptured(self, captured):
        ekind = ('acquire' if captured else 'release')
        info = self.newInfo(etype='capture', ekind=ekind, captured=captured)
        if self.addKeyMouseInfo(info):
            return False

        self.evtRoot.send(self.channelKey, info)
        return not info.get('skip', True)

