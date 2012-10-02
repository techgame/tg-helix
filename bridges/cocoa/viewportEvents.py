# -*- coding: utf-8 -*- vim: set ts=4 sw=4 expandtab
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2012  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

import sys
import Cocoa
from .common import CocoaEventSourceMixin

class CocoaViewportEventSource(CocoaEventSourceMixin):
    channelKey = 'viewport'

    def bindHost(self, glview, options):
        glview.events.bind('reshape', self.onEvtSize)
        glview.events.bind('paint', self.onEvtPaint)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onEvtSize(self):
        info = self.newInfo(viewSize=tuple(self.glview.frame().size))
        if not self.addKeyMouseInfo(info):
            return
        self.evtRoot.send(self.channelKey + '-size', info)

    def onEvtPaint(self, rect):
        info = self.newInfo(viewSize=tuple(self.glview.frame().size))
        if not self.addKeyMouseInfo(info):
            return
        self.evtRoot.send(self.channelKey + '-paint', info)

