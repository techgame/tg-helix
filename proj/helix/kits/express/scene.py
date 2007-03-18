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
from TG.helix.actors import HelixScene
from TG.helix.actors import sceneManagers

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpressNode(HelixNode):
    nodeKey = None

    @staticmethod # klass is passed in explicitly
    def nodeBuilder(klass, item):
        # try the node cache on the item itself
        sgItemNodes = getattr(item, 'sgNodes', None)

        if sgItemNodes is not None:
            node = sgItemNodes.get(klass.nodeKey, None)
            if node is not None:
                return node

        # get the graph op factory for the item.
        # should be compatable with ExpressGraphOp in stage module
        sgOpFactory = item.sceneGraphOps[klass.nodeKey]

        # create the scene graph op for the item
        if sgOpFactory:
            sgOp = sgOpFactory(item)
        else: sgOp = None

        # create the scene graph node for the op
        node = klass(sgOp)

        if sgItemNodes is not None:
            # cache it in item.sgNodes, so the item itself can get back to it
            sgItemNodes[klass.nodeKey] = node
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

