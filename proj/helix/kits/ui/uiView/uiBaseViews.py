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

from functools import partial

from TG.openGL.data import Vector
from TG.openGL.raw.gl import *

from TG.helix.framework.viewFactory import HelixViewFactory
from TG.helix.framework.views import HelixView
from TG.helix.framework.scene import HelixScene

from TG.helix.bridges.eventSource import EventRoot
from TG.helix.bridges.viewportEvents import GLViewportEventHandler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

uiViewFactory = HelixViewFactory()

class UIScene(HelixScene):
    viewForKeys = ['UIStage']
    viewFactory = uiViewFactory

    def __init__(self, stage=None):
        super(UIScene, self).__init__()
        self.init(stage)

    @classmethod
    def fromViewable(klass, stage):
        return klass(stage)

    def init(self, stage):
        if not stage.isHelixStage():
            raise ArgumentError("Expected an object supporting helix stage protocol")

        self.stage = stage
        self.stage.loadForScene(self)
        self.views = self.viewListFor(stage.items)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def resize(self, size):
        self.render()

        size = Vector(size+(0.,))
        for view in self.views:
            view.resize(size)
        return True

    def refresh(self):
        self.render()
        for view in self.views:
            view.render()
        return True

    glClearBuffers = staticmethod(partial(glClear, GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT))
    def render(self):
        self.glClearBuffers()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    evtRoot = EventRoot.property()
    def setupEvtSources(self, evtSources=[]):
        evtRoot = self.evtRoot
        evtRoot.addSourceGroup(evtSources)
        evtRoot.addHandler(GLViewportEventHandler(self))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIView(HelixView):
    viewForKeys = []
    viewFactory = uiViewFactory

    def __init__(self, viewable=None):
        super(UIView, self).__init__()
        self.init(viewable)

    @classmethod
    def fromViewable(klass, viewable):
        view = getattr(viewable, '__ui_view', None)
        if view is None:
            view = klass(viewable)
            setattr(viewable, '__ui_view', view)
        return view

    def init(self, viewable):
        if viewable is not None:
            viewable._pub_.add(self._onViewableChange)
        self._queueActions = []

    def _onViewableChange(self, viewable, attr):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def resize(self, size):
        pass
    def render(self):
        self.performQueueActions()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def enqueue(self, fn, *args):
        self.dequeue(fn)
        self._queueActions.append((fn, args))
    def dequeue(self, fn):
        itemsToRemove = [e for e in self._queueActions if e[0] == fn]
        for e in itemsToRemove:
            self._queueActions.remove(e)
    def performQueueActions(self):
        queue = self._queueActions[:]
        self._queueActions[:] = []

        for fnAction, args in queue:
            fnAction(*args)

