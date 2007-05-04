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

    def isSceneGraphOp(self):
        return True

    def init(self, node, actor): 
        pass

    def bindOp(self, node, opKey):
        node.bindPass.add(opKey, self._sgBindPass_)

    def _sgBindPass_(self, node, ct, srm): 
        pass

class SGResizeOp(SceneGraphOp):
    def init(self, node, actor): 
        self.res = node.res

    def _sgBindPass_(self, node, ct, srm):
        ct.add(self.resize)

    def resize(self, srm):
        pass

class SGRenderOp(SceneGraphOp):
    def init(self, node, actor): 
        self.res = node.res

    def _sgBindPass_(self, node, ct, srm):
        ct.add(self.render)

    def render(self, srm):
        pass

class SGLoadOp(SceneGraphOp):
    loaded = False
    actor = None
    def init(self, node, actor): 
        self.res = node.res
        self.actor = actor.asWeakProxy()
        return None

    def _sgBindPass_(self, node, ct, srm):
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
            Cell=MatuiCell)
    _sgOps_ = []

    _sgNode_ = None

    def isLayout(self): return False

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

        self._sgCellSetup_(node)
        self._sgOpSetup_(node)

    def _sgCellSetup_(self, node):
        Cell = getattr(self._fm_, 'Cell', None)
        if Cell is not None:
            self.cell = Cell(self)

    def _sgOpSetup_(self, node):
        sgOpsList = self._sgOps_
        if isinstance(sgOpsList, dict):
            sgOpsList = sgOpsList.items()

        for sgOp in sgOpsList:
            if isinstance(sgOp, str):
                opKey = sgOp
                opBind = 'sg_' + sgOp
            else: opKey, opBind = sgOp

            if isinstance(opBind, str):
                opFn = getattr(self, opBind)
                def bindOpFn(node, ct, srm, opFn=opFn):
                    ct.add(opFn)
                node.bindPass.add(opKey, bindOpFn)
            else:
                opBind(node, self, opKey)

