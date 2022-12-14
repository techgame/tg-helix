##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2009  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.helix.actors.theater import TheaterRenderContext

from .viewportEvents import qtViewportEventSource
from .keyboardEvents import qtKeyboardEventSource
from .mouseEvents import qtMouseEventSource
from .systemEvents import qtSystemEventSource
from .timerEvents import qtTimerEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtGLWidgetRenderContext(TheaterRenderContext):
    def __init__(self, glHost):
        glWidget = glHost.getGLWidget()
        self.glWidget = glWidget
    def getViewportSize(self):
        s = self.glWidget.size()
        return (s.width(), s.height())
    def select(self):
        self.glWidget.makeCurrent()
    def renderComplete(self, passKey):
        # we don't swap buffers, because QGLWidget will do it for us
        self.glWidget.swapBuffers()
    def animateRender(self):
        # mark the glWidget for redrawing, and return False
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Qt QGLWidget Helix Loader
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtHelixTheaterQGLWidgetLoader(object):
    RenderContext = qtGLWidgetRenderContext

    @classmethod
    def load(klass, glHost, options, theater, **kwsetup):
        glHost.setAutoBufferSwap(False)

        renderContext = klass.RenderContext(glHost)
        renderContext.select()

        theater.setup(renderContext)

        sources = klass.loadEvtSources(glHost, options, theater)
        return sources

    @classmethod
    def loadEvtSources(klass, glHost, options, theater):
        return [
            qtViewportEventSource(glHost, options, theater),
            qtSystemEventSource(glHost, options, theater),
            qtTimerEventSource(glHost, options, theater), 
            qtMouseEventSource(glHost, options, theater),
            qtKeyboardEventSource(glHost, options, theater), ]

TheaterHostViewLoader = qtHelixTheaterQGLWidgetLoader

