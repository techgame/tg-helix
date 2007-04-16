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

from TG.metaObserving import obInstProperty, OBFactoryMap
from TG.kvObserving import KVObject, KVProperty

from TG.helix.actors import HelixActor

from .node import MatuiNode

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphOp(object):
    _sgOp_ = None

    cullStack = False
    partial = staticmethod(partial)
    def __init__(self, node, actor): 
        self.init(node, actor)

    def init(self, node, actor): 
        pass
    def bindPass(self, node, sgo): 
        return None, None

class SGResizeOp(SceneGraphOp):
    def init(self, node, actor): 
        self.res = node.res

    def bindPass(self, node, sgo):
        return [self.resize], None

    def resize(self, sgo):
        pass

class SGRenderOp(SceneGraphOp):
    def init(self, node, actor): 
        self.res = node.res

    def bindPass(self, node, sgo):
        return [self.render], None

    def render(self, sgo):
        pass

class SGLoadOp(SceneGraphOp):
    actor = None
    def init(self, node, actor): 
        self.res = node.res
        self.actor = actor.asWeakProxy()
        return None

    def bindPass(self, node, sgo): 
        del node.loadPass
        return [self.load], None

    def load(self, sgo):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Actor
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiActor(HelixActor, KVObject):
    _fm_ = OBFactoryMap(Node=MatuiNode)
    _sgNode_ = KVProperty(None)
    _sgOps_ = {
        #'load': SGLoadOp, 
        #'render': SGRenderOp, 
        #'resize': None, 
        #'select': None,
        }

    def _sgNewNode_(self, **kw):
        node = self._sgNode_
        if node is not None:
            if not kw.get('force', False):
                return node

        node = self._fm_.Node()
        self._sgNode_ = node
        self._sgNodeSetup_(node)
        self._sgOpSetup_(node)
        return node

    def _sgNodeSetup_(self, node):
        node.actor = self
        node.res = {}

    def _sgOpSetup_(self, node):
        for sgOpKey, sgOpFactory in self._sgOps_.items():
            if sgOpFactory is not None: 
                sgOp = sgOpFactory(node, self)

                sgOpKey += 'Pass'
                setattr(node, sgOpKey, sgOp)

        if getattr(node, 'selectPass', None) is None:
            renderPass = getattr(node, 'renderPass', None)
            if renderPass is not None:
                node.selectPass = renderPass


