# -*- coding: utf-8 -*- vim: set ts=4 sw=4 expandtab
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2012  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

from TG.helix.actors.theater import TheaterRenderContext
from .viewportEvents import Win32ViewportEventSource
from .keyboardEvents import Win32KeyboardEventSource
from .systemEvents import Win32SystemEventSource
from .mouseEvents import Win32MouseEventSource
from .timerEvents import Win32TimerEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Win32TheaterRenderContext(TheaterRenderContext):
    def __init__(self, glwin):
        self.glwin = glwin
    def getViewportSize(self):
        return tuple(self.glwin.clientRect.size)
    def select(self):
        self.glwin.makeCurrentContext()
    def renderComplete(self, passKey):
        self.glwin.swapBuffers()
    def animateRender(self):
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Win32HelixTheaterHostViewLoader(object):
    @classmethod
    def load(klass, glwin, options, theater, **kwsetup):
        renderContext = Win32TheaterRenderContext(glwin)
        renderContext.select()

        theater.setup(renderContext)

        sources = klass.loadEvtSources(glwin, options, theater)
        return sources

    @classmethod
    def loadEvtSources(self, glwin, options, theater):
        return [
            Win32ViewportEventSource(glwin, options, theater),
            Win32MouseEventSource(glwin, options, theater),
            Win32KeyboardEventSource(glwin, options, theater),
            Win32SystemEventSource(glwin, options, theater),
            Win32TimerEventSource(glwin, options, theater),
            ]

TheaterHostViewLoader = Win32HelixTheaterHostViewLoader

