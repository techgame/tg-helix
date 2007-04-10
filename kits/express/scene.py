##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2007  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.helix.actors import HelixNode
from TG.helix.actors import sceneManagers
from TG.helix.actors.scene import HelixScene, SceneAnimationEventHandler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpressNode(HelixNode):
    nodeKey = None

    @classmethod
    def itemAsNode(klass, item, create=True):
        if item.isNode():
            return item

        nodeKey = klass.nodeKey
        node = item.sceneGraphNodes.get(nodeKey, None)
        if node is None and create:
            node = item.sceneNodeFor(nodeKey, klass.new())
        return node

class RenderNode(ExpressNode):
    nodeKey = 'render'

class ResizeNode(ExpressNode):
    nodeKey = 'resize'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpressScene(HelixScene):
    sgPassFactories = {
        'render': (RenderNode, sceneManagers.RenderManager),
        'resize': (ResizeNode, sceneManagers.ResizeManager),
        }

    def setupEvtSources(self, evtSources=[]):
        evtRoot = HelixScene.setupEvtSources(self, evtSources)
        evtRoot.visit(SceneAnimationEventHandler(self))
        return evtRoot

    def setupSceneGraph(self):
        for kind, (nodeType, managerFactory) in self.sgPassFactories.iteritems():
            rootNode = nodeType.createRootForScene(self)
            manager = managerFactory(self, rootNode)
            self.sgManagers[kind] = manager

    meter = property(lambda self: self)
    def start(self): 
        tsStart = self.timestamp()
        if not self.nframes:
            self._tsStart = tsStart
            self._tsCum = 0.0
        return tsStart
    def end(self, tsStart): 
        tsEnd = self.timestamp()
        self._tsCum += tsEnd - tsStart

        n = self.nframes + 1
        if not (n % 60):
            ts = self._tsStart
            print n/(tsEnd-ts), 60./self._tsCum
            self._tsCum = 0.0
        self.nframes = n
    nframes = 0

