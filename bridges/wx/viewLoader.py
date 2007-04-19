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
    def load(klass, glviewhost, options, scene, **kwsetup):
        glviewhost.SetCurrent()

        # Reload the opengl raw api to support windows
        TG.openGL.raw.apiReload()

        evtSources = klass.loadEvtSources(glviewhost, options)
        scene.setup(evtSources=evtSources, **kwsetup)
        #evtSources[0].sendSize(tuple(glviewhost.GetClientSize()))
        #evtSources[0].sendPaint()
        return scene

    @classmethod
    def loadEvtSources(self, glviewhost, options):
        return [
            wxViewportEventSource(glviewhost, options),
            wxMouseEventSource(glviewhost, options),
            wxKeyboardEventSource(glviewhost, options),
            wxTimerEventSource(glviewhost, options),
            wxIdleEventSource(glviewhost, options),
            ]

SceneHostViewLoader = wxHelixSceneHostViewLoader

