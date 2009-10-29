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

from ..qt.viewportEvents import qtViewportEventSource
from ..qt.keyboardEvents import qtKeyboardEventSource
from ..qt.systemEvents import qtSystemEventSource
from ..qt.timerEvents import qtTimerEventSource
from .mouseEvents import qtGraphicsViewMouseEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtGLGraphicsViewRenderContext(TheaterRenderContext):
    def __init__(self, glHost):
        glWidget = glHost.getGLWidget()
        self.qtScene = glHost.scene()
        self.glWidget = glWidget
    def getViewportSize(self):
        s = self.glWidget.size()
        return (s.width(), s.height())
    def select(self):
        self.glWidget.makeCurrent()
    def renderComplete(self, passKey):
        # we don't swap buffers, because QGLWidget will do it for us
        pass
    def animateRender(self):
        # mark the glWidget for redrawing, and return False
        self.glWidget.update()
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Qt GraphicsView Helix Loader
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtHelixTheaterQGLWidgetLoader(object):
    RenderContext = qtGLGraphicsViewRenderContext

    @classmethod
    def load(klass, glHost, options, theater, **kwsetup):
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
            qtGraphicsViewMouseEventSource(glHost, options, theater),
            qtKeyboardEventSource(glHost, options, theater), ]

TheaterHostViewLoader = qtHelixTheaterQGLWidgetLoader

