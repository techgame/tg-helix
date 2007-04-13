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

from functools import partial

from TG.kvObserving import KVObject, KVProperty
from TG.metaObserving import obInstProperty

from TG.helix.actors import HelixActor
from TG.helix.actors import HelixStage

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpressResources(object):
    _partial = staticmethod(partial)
    def __init__(self, actor):
        pass
    def load(self, sgNode, sgo):
        pass

ExpressResources.property = classmethod(obInstProperty)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpressGraphOp(object):
    cullStack = False
    def __init__(self, actor, sgNode): 
        pass
    def bindPass(self, sgNode, sgo): 
        return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpressActor(HelixActor, KVObject):
    sceneGraphOps = {'render': None, 'resize': None}
    sceneGraphNodes = KVProperty(dict)

    def sceneNodeFor(self, nodeKey, node):
        self.sceneGraphNodes[nodeKey] = node

        sgpi = self.sceneGraphOpFor(nodeKey, node)
        setattr(node, nodeKey+'Pass', sgpi)

        return node

    def sceneGraphOpFor(self, sgOpKey, sgNode):
        sgOpFactory = self.sceneGraphOps.get(sgOpKey, None)
        if sgOpFactory is not None:
            return sgOpFactory(self, sgNode)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpressStage(HelixStage, KVObject):
    box = KVProperty(None)

    def onSceneSetup(self, scene):
        self._setupBackground(scene)

    def _setupBackground(self, scene):
        from . import actors

        sgnResize = scene['resize']
        sgnRender = scene['render']

        viewport = actors.Viewport()
        sgnResize += viewport
        sgnRender += viewport

        projection = actors.Projection()
        sgnResize += projection
        sgnRender += projection

        bgLayer = actors.BackgroundLayer()
        bgLayer.box.viewOf(projection.box, dim=2)
        sgnRender += bgLayer
        self.box = bgLayer.box

        self.root = actors.Group()
        sgnRender += self.root

    def onSceneShutdown(self, scene):
        pass

    def onSceneAnimate(self, scene, info):
        return True

