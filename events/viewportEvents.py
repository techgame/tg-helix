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

class ViewportEventSource(HostViewEventSource):
    kind = 'viewport'

    def sendSize(self, size):
        for eh in self.iterHandlers():
            r = eh.resize(self, size)
            if r is not None:
                return r

    def sendErase(self):
        for eh in self.iterHandlers():
            r = eh.erase(self)
            if r is not None:
                return r

    def sendPaint(self):
        for eh in self.iterHandlers():
            r = eh.paint(self)
            if r is not None:
                return r

    def sendInitial(self):
        size = self.getViewSize()
        for eh in self.iterHandlers():
            r = eh.initial(self, size)
            if r is not None:
                return r

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewportEventHandler(EventHandler):
    eventKinds = ['viewport']

    def initial(self, hostview, viewportSize):
        pass
    def resize(self, hostview, viewportSize):
        pass
    def erase(self, hostview):
        pass
    def paint(self, hostview):
        pass

