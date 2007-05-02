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

from TG.helix.actors.scene import SceneRenderContext
from .viewportEvents import wxViewportEventSource
from .keyboardEvents import wxKeyboardEventSource
from .mouseEvents import wxMouseEventSource
from .timerEvents import wxTimerEventSource, wxIdleEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxSceneRenderContext(SceneRenderContext):
    def __init__(self, glCanvas):
        self.glCanvas = glCanvas
    def getSize(self):
        return tuple(self.glCanvas.GetClientSize())
    def select(self):
        self.glCanvas.SetCurrent()
    def swap(self):
        self.glCanvas.SwapBuffers()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxHelixSceneHostViewLoader(object):
    @classmethod
    def load(klass, glCanvas, options, scene, **kwsetup):
        renderContext = wxSceneRenderContext(glCanvas)
        renderContext.select()

        # Reload the opengl raw api to support windows
        TG.openGL.raw.apiReload()

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

SceneHostViewLoader = wxHelixSceneHostViewLoader

