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

from .base import HelixObject
from . import sceneManagers

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixScene(HelixObject):
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

    def init(self, stage):
        self.stage = stage
        self.evtRoot = self.EventRootFactory()

        self.sgManagers = {}
        self.sgNodes = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setup(self, evtSources=[], **kwinfo):
        self.setupManagers()
        self.setupEvtSources(evtSources)
        self.stage.onSceneSetup(self)
        return True

    EventRootFactory = None #SceneEventRoot
    evtRoot = None
    def setupEvtSources(self, evtSources=[]):
        self.evtRoot.configFor(self, evtSources)

    def setupSceneGraph(self):
        self.sgManagers.update(
            render=sceneManagers.RenderManager(self),
            resize=sceneManagers.ResizeManager(self),
            select=sceneManagers.SelectManager(self),
            )

    def shutdown(self):
        self.stage.onSceneShutdown(self)
        return True

Scene = HelixScene

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene Event adaptations 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneEventRoot(EventRoot):
    def configFor(self, scene, evtSources):
        self.visitGroup(evtSources)

        self.visit(SceneViewportEventHandler(scene))

HelixScene.EventRootFactory = SceneEventRoot

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
        self.stage = scene.stage
        self.sgManagers = scene.sgManagers

    def timer(self, viewport, info):
        if stage.onAnimateEvent(info):
            return self.sgManagers['render'](viewport)

