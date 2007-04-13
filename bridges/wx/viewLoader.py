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

import TG.openGL.raw

from .viewportEvents import wxViewportEventSource
from .keyboardEvents import wxKeyboardEventSource
from .mouseEvents import wxMouseEventSource
from .timerEvents import wxTimerEventSource, wxIdleEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxHelixSceneHostViewLoader(object):
    @classmethod
    def load(klass, glviewhost, stage, scene, **kwsetup):
        glviewhost.SetCurrent()

        # Reload the opengl raw api to support windows
        TG.openGL.raw.apiReload()

        evtSources = klass.loadEvtSources(glviewhost, stage)

        scene.setup(evtSources=evtSources, **kwsetup)

        evtSources[0].sendSize(tuple(glviewhost.GetClientSize()))
        evtSources[0].sendPaint()
        return scene

    @classmethod
    def loadEvtSources(self, glviewhost, stage):
        return [
            wxViewportEventSource(glviewhost, stage),
            wxMouseEventSource(glviewhost, stage),
            wxKeyboardEventSource(glviewhost, stage),
            wxTimerEventSource(glviewhost, stage),
            wxIdleEventSource(glviewhost, stage),
            ]

SceneHostViewLoader = wxHelixSceneHostViewLoader

