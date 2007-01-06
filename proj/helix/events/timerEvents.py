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

from .eventSource import EventHandler, HostViewEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TimerEventSource(HostViewEventSource):
    kind = 'timer'

    def sendTimer(self, info):
        for eh in self.iterHandlers():
            r = eh.timer(self, info)
            if r is not None:
                return r

class TimerEventHandler(EventHandler):
    eventKinds = ['timer']

    def timer(self, hostview, info):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IdleEventSource(HostViewEventSource):
    kind = 'idle'

    def sendIdle(self, info):
        for eh in self.iterHandlers():
            r = eh.idle(self, info)
            if r is not None:
                return r

class IdleEventHandler(EventHandler):
    eventKinds = ['idle']

    def idle(self, hostview, info):
        pass

