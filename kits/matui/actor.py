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
from .layout import MatuiCell

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphOp(object):
    _sgOp_ = None

    cullStack = False
    partial = staticmethod(partial)
    def __init__(self, node, actor, opKey): 
        self.init(node, actor)
        self.bindOp(node, opKey)

    def init(self, node, actor): 
        pass

    def bindOp(self, node, opKey):
        setattr(node, opKey+'Pass', self)

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
    loaded = False
    actor = None
    def init(self, node, actor): 
        self.res = node.res
        self.actor = actor.asWeakProxy()
        return None

    def bindPass(self, node, sgo): 
        if not self.loaded:
            return [self.loadOp], None
        else: return None, None

    def loadOp(self, sgo):
        self.load(sgo)
        self.loaded = True
    def load(self, sgo):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Actor
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiActor(HelixActor, KVObject):
    _fm_ = OBFactoryMap(
            Node=MatuiNode, 
            Cell=MatuiCell)
    _sgOps_ = {}

    _sgNode_ = None

    def _sgGetNode_(self, create=True):
        node = self._sgNode_
        if not create:
            return node

        if node is None:
            node = self._fm_.Node()
            self._sgNodeSetup_(node)

        return node

    def _sgNodeSetup_(self, node):
        self._sgNode_ = node
        node.actor = self
        node.res = {}
        self._sgCellSetup_(node)
        self._sgOpSetup_(node)

    def _sgCellSetup_(self, node):
        Cell = getattr(self._fm_, 'Cell', None)
        if Cell is not None:
            self.cell = Cell(self.asWeakRef())

    def _sgOpSetup_(self, node):
        for sgOpKey, sgOpSetup in self._sgOps_.items():
            if sgOpSetup is not None: 
                sgOpSetup(node, self, sgOpKey)

