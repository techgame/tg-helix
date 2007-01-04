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

from .eventSource import GLEventSource
from .eventChain import EventHandler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GLViewportEventSource(GLEventSource):
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

class GLViewportEventHandler(EventHandler):
    eventKinds = ['viewport']

    def initial(self, glview, viewportSize):
        pass
    def resize(self, glview, viewportSize):
        pass
    def erase(self, glview):
        pass
    def paint(self, glview):
        pass

