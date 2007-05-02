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

from . import base, node, events, sceneManagers

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneRenderContext(object):
    def getSize(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def select(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def swap(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixScene(base.HelixObject):
    """A Helix Scene is a mediator, tieing viewport, events, and managers together in an extensible way.
    
    The sgPass are called on by the events to handle rendering, resizing, and
    selection operations over the scene's nodes."""

    _fm_ = OBFactoryMap(
            Node = node.HelixNode,
            EventRoot = events.EventRoot,

            sg_factories = {
                'load': sceneManagers.LoadManager,
                'render': sceneManagers.RenderManager,
                'resize': sceneManagers.ResizeManager,
                'select': sceneManagers.SelectManager,
                },
            )

    def isScene(self): return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self):
        self.init()

    def init(self):
        self.sgPass = {}
        self.root = self._fm_.Node(scene=self)
        self.evtRoot = self._fm_.EventRoot()
        self.timestamp = self.evtRoot.newTimestamp

    def setup(self, renderContext):
        self.renderContext = renderContext
        self.setupSceneGraph()
        self.setupEvtSources()
        return True

    def setupSceneGraph(self):
        sg_factories = self._fm_.sg_factories
        for key, factory in sg_factories.items():
            self.sgPass[key] = factory(self)

    def setupEvtSources(self):
        pass

