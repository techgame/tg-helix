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
from .systemEvents import qtSystemEventSource
from .mouseEvents import qtMouseEventSource
from .timerEvents import qtTimerEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtTheaterRenderContext(TheaterRenderContext):
    def __init__(self, glWidget):
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

class qtHelixTheaterHostViewLoader(object):
    @classmethod
    def load(klass, glHost, options, theater, **kwsetup):
        glWidget = glHost.getGLWidget()
        renderContext = qtTheaterRenderContext(glWidget)
        renderContext.select()

        theater.setup(renderContext)

        sources = klass.loadEvtSources(glHost, options, theater)
        return sources

    @classmethod
    def loadEvtSources(self, glHost, options, theater):
        return [
            qtViewportEventSource(glHost, options, theater),
            qtMouseEventSource(glHost, options, theater),
            qtKeyboardEventSource(glHost, options, theater),
            qtSystemEventSource(glHost, options, theater),
            qtTimerEventSource(glHost, options, theater),
            ]

TheaterHostViewLoader = qtHelixTheaterHostViewLoader

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtHostMixin(object):
    # viewport delegate
    dgViewport = None

    def setHelixViewportDelegate(self, dgViewport):
        self.dgViewport = dgViewport
    def initializeGL(self):
        return self.dgViewport.initializeGL()
    def resizeGL(self, w, h):
        return self.dgViewport.resizeGL(w, h)
    def paintGL(self):
        return self.dgViewport.paintGL()

    _eventRegistry = None
    def getEventRegistry(self):
        reg = self._eventRegistry
        if reg is None:
            reg = {}
            self._eventRegistry = reg
        return reg
    eventRegistry = property(getEventRegistry)

    def bindEvent(self, key, fn):
        self.eventRegistry[key] = fn

    def _dispatchRegisteredEvent(self, evt):
        et = evt.type(); ek = evt.__class__
        reg = self.eventRegistry
        fns = []
        for key in [(et, ek), et, ek]:
            fn = reg.get(key)
            if fn is not None:
                fns.append(fn)

        if fns:
            self.makeCurrent()
            for fn in fns:
                r = fn(evt)
                if r: 
                    return r

    def event(self, evt):
        r = self._dispatchRegisteredEvent(evt)
        if not r:
            r = super(qtHostMixin, self).event(evt)
        return r

