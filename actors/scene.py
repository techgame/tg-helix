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

from ..events.eventSource import EventRoot
from ..events.viewportEvents import ViewportEventHandler
from ..events.timerEvents import TimerEventHandler

from . import base, node, sceneManagers

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixScene(base.HelixObject):
    """A Helix Scene is a mediator, tieing viewport, events, and managers together in an extensible way.
    
    The sgManagers are called on by the events to handle rendering, resizing, and
    selection operations over the scene's stage object.  The stage is the
    scene's link to the web of actors that are set in the stage, but is mostly
    used to allow customization of the creation and setup process without
    having to understand all of the details of a Scene and it's various objects.
    """
    stage = None

    def isScene(self): return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, stage):
        self.init(stage)

    def __repr__(self):
        return '%s: %r' % (self.__class__.__name__, self.stage)

    def __getitem__(self, key):
        return self.sgManagers[key].root
    def __setitem__(self, key, value):
        # provided for convinence only... value must be
        # what is already stored there
        return self.sgManagers[key].root
    def get(self, key, default=None):
        return self.sgManagers[key].root

    def init(self, stage):
        self.stage = stage
        self.evtRoot = self.EventRootFactory()
        self.sgManagers = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setup(self, evtSources=[], **kwinfo):
        self.setupEvtSources(evtSources)
        self.setupSceneGraph()
        self.stage.onSceneSetup(self)
        return True

    EventRootFactory = EventRoot
    evtRoot = None
    def setupEvtSources(self, evtSources=[]):
        evtRoot = self.evtRoot
        evtRoot.visitGroup(evtSources)
        self.timestamp = evtRoot.newTimestamp

        evtRoot.visit(SceneViewportEventHandler(self))
        return evtRoot

    def setupSceneGraph(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def shutdown(self):
        self.stage.onSceneShutdown(self)
        return True

    def animate(self, info):
        return self.stage.onSceneAnimate(self, info)

Scene = HelixScene

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene Event adaptations 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneViewportEventHandler(ViewportEventHandler):
    def __init__(self, scene):
        self.sgManagers = scene.sgManagers

    def resize(self, viewport, viewportSize):
        return self.sgManagers['resize'](viewport, viewportSize)

    def erase(self, viewport):
        return True

    def paint(self, viewport):
        return self.sgManagers['render'](viewport)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneAnimationEventHandler(TimerEventHandler):
    def __init__(self, scene):
        self.scene = scene
        self.sgManagers = scene.sgManagers

    def timer(self, viewport, info):
        if self.scene.animate(info):
            return self.sgManagers['render'](viewport)

