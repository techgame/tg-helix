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

from TG.helix.actors.theater import TheaterRenderContext
from .viewportEvents import wxViewportEventSource
from .keyboardEvents import wxKeyboardEventSource
from .systemEvents import wxSystemEventSource
from .mouseEvents import wxMouseEventSource
from .timerEvents import wxTimerEventSource, wxIdleEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxTheaterRenderContext(TheaterRenderContext):
    def __init__(self, glCanvas):
        self.glCanvas = glCanvas
    def getViewportSize(self):
        return tuple(self.glCanvas.GetClientSize())
    def select(self):
        self.glCanvas.SetCurrent()
    def renderComplete(self, passKey):
        self.glCanvas.SwapBuffers()
    def animateRender(self):
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxHelixTheaterHostViewLoader(object):
    @classmethod
    def load(klass, glCanvas, options, theater, **kwsetup):
        renderContext = wxTheaterRenderContext(glCanvas)
        renderContext.select()

        theater.setup(renderContext)

        sources = klass.loadEvtSources(glCanvas, options, theater)
        return sources

    @classmethod
    def loadEvtSources(self, glCanvas, options, theater):
        return [
            wxViewportEventSource(glCanvas, options, theater),
            wxMouseEventSource(glCanvas, options, theater),
            wxKeyboardEventSource(glCanvas, options, theater),
            wxSystemEventSource(glCanvas, options, theater),
            wxTimerEventSource(glCanvas, options, theater),
            wxIdleEventSource(glCanvas, options, theater),
            ]

TheaterHostViewLoader = wxHelixTheaterHostViewLoader

