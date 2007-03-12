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
    key = None

    @staticmethod
    def nodeBuilder(klass, item):
        sgOp = item.sceneGraphOps[klass.key](item)
        node = klass(sgOp)
        item.nodes[klass.key] = node
        return node

class RenderNode(ExpressNode):
    key = 'render'

class ResizeNode(HelixNode):
    key = 'resize'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpressScene(HelixScene):
    sgPassFactories = {
        'render': (RenderNode, sceneManagers.RenderManager),
        'resize': (ResizeNode, sceneManagers.ResizeManager),
        }

