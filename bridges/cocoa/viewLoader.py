# -*- coding: utf-8 -*- vim: set ts=4 sw=4 expandtab
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2012  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

from TG.helix.actors.theater import TheaterRenderContext
#from .viewportEvents import CocoaViewportEventSource
#from .keyboardEvents import CocoaKeyboardEventSource
#from .systemEvents import CocoaSystemEventSource
#from .mouseEvents import CocoaMouseEventSource
#from .timerEvents import CocoaTimerEventSource, CocoaIdleEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CocoaTheaterRenderContext(TheaterRenderContext):
    def __init__(self, glView):
        self.glView = glView
    def getViewportSize(self):
        return tuple(self.glView.frame.size)
    def select(self):
        self.glView.openGLContext().makeCurrentContext()
    def renderComplete(self, passKey):
        self.glView.openGLContext().flushBuffer()
    def animateRender(self):
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CocoaHelixTheaterHostViewLoader(object):
    @classmethod
    def load(klass, glCanvas, options, theater, **kwsetup):
        renderContext = CocoaTheaterRenderContext(glCanvas)
        renderContext.select()

        theater.setup(renderContext)

        sources = klass.loadEvtSources(glCanvas, options, theater)
        return sources

    @classmethod
    def loadEvtSources(self, glCanvas, options, theater):
        return [
            CocoaViewportEventSource(glCanvas, options, theater),
            CocoaMouseEventSource(glCanvas, options, theater),
            CocoaKeyboardEventSource(glCanvas, options, theater),
            CocoaSystemEventSource(glCanvas, options, theater),
            CocoaTimerEventSource(glCanvas, options, theater),
            CocoaIdleEventSource(glCanvas, options, theater),
            ]

TheaterHostViewLoader = CocoaHelixTheaterHostViewLoader

