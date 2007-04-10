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

from TG.helix.events.eventSource import EventRoot
from TG.helix.events.viewportEvents import ViewportEventHandler
from TG.helix.events.timerEvents import TimerEventHandler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiEventRoot(EventRoot):
    def configFor(self, scene, evtSources):
        self += evtSources

        self += MatuiViewportEventHandler(scene)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiViewportEventHandler(ViewportEventHandler):
    def __init__(self, scene):
        self.scene = scene
        self.sceneManagers = scene.managers

    def resize(self, hostView, viewportSize):
        resizeManager = self.sceneManagers['resize']
        return resizeManager.resize(hostView, viewportSize)

    def erase(self, hostView):
        return True

    def paint(self, hostView):
        renderManager = self.scene.managers['render']
        return renderManager.render(hostView)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiAnimationEventHandler(TimerEventHandler):
    def __init__(self, scene):
        self.scene = scene
        self.sceneManagers = scene.managers

    def timer(self, hostView, info):
        scene = self.scene
        if scene.stage.onSceneAnimate(scene, hostView, info):
            renderManager = self.sceneManagers['render']
            return renderManager.render(hostView)

