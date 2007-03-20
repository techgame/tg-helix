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
        node = klass._treeItemAsNodeCache.get(item, None)
        if not create or node is not None:
            return node

        node = klass()
        sgpi = item.sceneGraphOpFor(klass.nodeKey, node)
        setattr(node, klass.nodeKey+'Pass', sgpi)
        klass._treeItemAsNodeCache[item] = node
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
        super(ExpressScene, self).setupEvtSources(evtSources)
        self.evtRoot.visit(SceneAnimationEventHandler(self))

