# -*- coding: utf-8 -*- vim: set ts=4 sw=4 expandtab
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2012  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

import Cocoa
from .common import CocoaEventSourceMixin

class CocoaSystemEventSource(CocoaEventSourceMixin):
    channelKey = 'system'

    def bindHost(self, glview, options):
        nc = Cocoa.NSNotificationCenter.defaultCenter()
        nc.addObserver_selector_name_object_(
            self, 'onEvtAppActivate:', Cocoa.NSApplicationDidBecomeActiveNotification, None)
        nc.addObserver_selector_name_object_(
            self, 'onEvtAppDeactivate:', Cocoa.NSApplicationDidResignActiveNotification, None)
        nc.addObserver_selector_name_object_(
            self, 'onEvtWinActivate:', Cocoa.NSWindowDidBecomeMainNotification, None)
        nc.addObserver_selector_name_object_(
            self, 'onEvtWinDeactivate:', Cocoa.NSWindowDidResignMainNotification, None)

    def onEvtAppActivate_(self, notification):
        self._sendEvent('app', 'activate', True)
    def onEvtAppDeactivate_(self, notification):
        self._sendEvent('app', 'deactivate', False)

    def onEvtWinActivate_(self, notification):
        self._sendEvent('window', 'activate', True)
    def onEvtWinDeactivate_(self, notification):
        self._sendEvent('window', 'deactivate', False)

    def _sendEvent(self, etype, ekind, active):
        info = self.newInfo(etype=etype, ekind=ekind, active=active)
        if not self.addKeyMouseInfo(info):
            return
        self.evtRoot.send(self.channelKey, info)

