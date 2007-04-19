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

from TG.metaObserving import OBFactoryMap

from ..events import eventSource
from ..events.viewportEvents import ViewportEventHandler
from ..events.timerEvents import TimerEventHandler

from . import base, node, sceneManagers

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixScene(base.HelixObject):
    """A Helix Scene is a mediator, tieing viewport, events, and managers together in an extensible way.
    
    The sgPass are called on by the events to handle rendering, resizing, and
    selection operations over the scene's nodes."""

    _fm_ = OBFactoryMap(
            Node = node.HelixNode,
            EventRoot = eventSource.EventRoot,
            )

    _sgPassFactories_ = {
        'load': sceneManagers.LoadManager,
        'render': sceneManagers.RenderManager,
        'resize': sceneManagers.ResizeManager,
        'select': sceneManagers.SelectManager,
        }

    def isScene(self): return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self):
        self.init()

    def init(self):
        self.sgPass = {}
        self.root = self._fm_.Node(scene=self)
        self.evtRoot = self._fm_.EventRoot()
        self.timestamp = self.evtRoot.newTimestamp

    def setup(self, evtSources=[], **kwinfo):
        self.setupEvtSources(evtSources)
        self.setupSceneGraph()
        return True

    evtRoot = None
    def setupEvtSources(self, evtSources=[]):
        evtRoot = self.evtRoot
        evtRoot.visitGroup(evtSources)

        evtRoot.visit(SceneViewportEventHandler(self))
        evtRoot.visit(SceneAnimationEventHandler(self))
        return evtRoot

    def setupSceneGraph(self):
        root = self.root

        for sgPassKey, sgPassFactory in self._sgPassFactories_.items():
            sgPass = sgPassFactory(self, root.newParent())
            self.sgPass[sgPassKey] = sgPass

    def _sgResize_(self, viewport, viewportSize):
        self.sgPass['load'](viewport)
        return self.sgPass['resize'](viewport, viewportSize)
    def _sgRender_(self, viewport):
        self.sgPass['load'](viewport)
        return self.sgPass['render'](viewport)

    animate = False
    def _sgAnimate_(self, viewport, info):
        if self.animate:
            return self._sgRender_(viewport)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene Event adaptations 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneViewportEventHandler(ViewportEventHandler):
    def __init__(self, scene):
        self.scene = scene

    def resize(self, viewport, viewportSize):
        return self.scene._sgResize_(viewport, viewportSize)

    def erase(self, viewport):
        return True

    def paint(self, viewport):
        return self.scene._sgRender_(viewport)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneAnimationEventHandler(TimerEventHandler):
    def __init__(self, scene):
        self.scene = scene

    def timer(self, viewport, info):
        self.scene._sgAnimate_(viewport, info)

