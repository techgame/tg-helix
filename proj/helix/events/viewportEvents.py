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
            if eh.resize(self, size):
                return True

    def sendErase(self):
        for eh in self.iterHandlers():
            if eh.erase(self):
                return True

    def sendPaint(self):
        for eh in self.iterHandlers():
            if eh.paint(self):
                return True

    def sendInitial(self):
        size = self.getViewSize()
        for eh in self.iterHandlers():
            if eh.initial(self, size):
                return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GLViewportEventHandler(EventHandler):
    kind = 'viewport'
    scene = None

    def __init__(self, scene):
        if not scene.isHelixScene():
            raise ValueError("Viewport Event Handler requires a helix scene to work with")
        self.scene = scene

    def initial(self, glview, viewportSize):
        glview.setViewCurrent()
        if self.scene.refreshInitial(viewportSize):
            glview.viewSwapBuffers()
        return True

    def resize(self, glview, viewportSize):
        glview.setViewCurrent()
        if self.scene.resize(viewportSize):
            glview.viewSwapBuffers()
        return True

    def erase(self, glview):
        return True

    def paint(self, glview):
        glview.setViewCurrent()
        if self.scene.refresh():
            glview.viewSwapBuffers()
        return True

