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
from .mouseEvents import wxMouseEventSource
from .timerEvents import wxTimerEventSource, wxIdleEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxTheaterRenderContext(TheaterRenderContext):
    def __init__(self, glCanvas):
        self.glCanvas = glCanvas
    def getSize(self):
        return tuple(self.glCanvas.GetClientSize())
    def select(self):
        self.glCanvas.SetCurrent()
    def swap(self):
        self.glCanvas.SwapBuffers()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxHelixTheaterHostViewLoader(object):
    @classmethod
    def load(klass, glCanvas, options, scene, **kwsetup):
        renderContext = wxTheaterRenderContext(glCanvas)
        renderContext.select()

        scene.setup(renderContext)

        klass.loadEvtSources(glCanvas, options, scene)
        return scene

    @classmethod
    def loadEvtSources(self, glCanvas, options, scene):
        return [
            wxViewportEventSource(glCanvas, options, scene),
            wxMouseEventSource(glCanvas, options, scene),
            wxKeyboardEventSource(glCanvas, options, scene),
            wxTimerEventSource(glCanvas, options, scene),
            wxIdleEventSource(glCanvas, options, scene),
            ]

TheaterHostViewLoader = wxHelixTheaterHostViewLoader

