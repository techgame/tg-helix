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
from TG.geomath.data.kvBox import KVBox

from .node import MatuiNode

from .cell import MatuiCell

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphOp(object):
    _sgOp_ = None

    cullStack = False
    partial = staticmethod(partial)
    def __init__(self, actor, node, opKey): 
        self.init(node, actor)
        self.bindOp(node, opKey)

    def isSceneGraphOp(self):
        return True

    def init(self, node, actor): 
        pass

    def bindOp(self, node, opKey):
        node.addPass(opKey, self.sgPassBind)

    def _getNodeRes(self, node):
        res = getattr(node, 'res', None)
        if res is None:
            res = {}
            node.res = {}
        return res

    def sgPassBind(self, node, ct): 
        pass

class SGResizeOp(SceneGraphOp):
    def init(self, node, actor): 
        self.res = self._getNodeRes(node)

    def sgPassBind(self, node, ct):
        ct.add(self.resize)

    def resize(self, srm):
        pass

class SGRenderOp(SceneGraphOp):
    def init(self, node, actor): 
        self.res = self._getNodeRes(node)

    def sgPassBind(self, node, ct):
        ct.add(self.render)

    def render(self, srm):
        pass

class SGLoadOp(SceneGraphOp):
    loaded = False
    actor = None
    def init(self, node, actor): 
        node.res = {}
        self.res = self._getNodeRes(node)
        self.actor = actor.asWeakProxy()
        return None

    def sgPassBind(self, node, ct):
        if not self.loaded:
            ct.add(self.loadOp)

    def loadOp(self, srm):
        self.load(srm)
        self.loaded = True
    def load(self, srm):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Actor
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiActor(HelixActor, KVObject):
    _fm_ = OBFactoryMap(
            Node=MatuiNode, 
            Cell=MatuiCell,
            sgOpPrefix='sg_',
            )
    _sgOps_ = []

    node = None

    def isLayout(self): return False

    def _sgGetNode_(self, create=True):
        node = self.node
        if not create:
            return node

        if node is None:
            node = self._fm_.Node()
            self._sgNodeSetup_(node)

        return node

    def _sgNodeSetup_(self, node):
        self.node = node
        node.info = self.__class__.__name__
        Cell = self._fm_.Cell
        if Cell is not None:
            self.cell = Cell(self.asWeakProxy())

        self.sgAddOpList(self._sgOps_, node)


        node.actor_ref = self.asStrongRef()
        def cleanup(wr, nr=node.asWeakRef()): 
            node = nr()
            if node is not None: 
                node.clear()
        self._wr_cleanup = self.asWeakRef(cleanup)


    def sgAddOpList(self, opsList, node=None):
        if node is None: node = self.node

        if isinstance(opsList, dict):
            opsList = sorted(opsList.items())

        for op in opsList:
            if isinstance(op, str):
                opKey = op
                opBind = None
            else: opKey, opBind = op
            self.sgAddOp(opKey, opBind, node)


    def sgAddOp(self, opKey, opBind=None, node=None):
        if node is None: node = self.node

        if opBind is None:
            opBind = self._fm_.sgOpPrefix + opKey

        if isinstance(opBind, str):
            node.onPass(opKey, getattr(self, opBind))

        else:
            opBind(self, node, opKey)

    def sgClearOp(self, opKey):
        self.node.clearPass(opKey)

