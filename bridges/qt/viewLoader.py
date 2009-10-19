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
#from .keyboardEvents import qtKeyboardEventSource
#from .systemEvents import qtSystemEventSource
from .mouseEvents import qtMouseEventSource
from .timerEvents import qtTimerEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtTheaterRenderContext(TheaterRenderContext):
    def __init__(self, glCanvas):
        self.glCanvas = glCanvas
    def getSize(self):
        s = self.glCanvas.size()
        return (s.width(), s.height())
    def select(self):
        self.glCanvas.makeCurrent()
    def swap(self):
        self.glCanvas.swapBuffers()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtHelixTheaterHostViewLoader(object):
    @classmethod
    def load(klass, glCanvas, options, theater, **kwsetup):
        renderContext = qtTheaterRenderContext(glCanvas)
        renderContext.select()

        theater.setup(renderContext)

        sources = klass.loadEvtSources(glCanvas, options, theater)
        return sources

    @classmethod
    def loadEvtSources(self, glCanvas, options, theater):
        return [
            qtViewportEventSource(glCanvas, options, theater),
            qtMouseEventSource(glCanvas, options, theater),
            #qtKeyboardEventSource(glCanvas, options, theater),
            #qtSystemEventSource(glCanvas, options, theater),
            qtTimerEventSource(glCanvas, options, theater),
            ]

TheaterHostViewLoader = qtHelixTheaterHostViewLoader

