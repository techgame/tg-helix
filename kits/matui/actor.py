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

from TG.kvObserving import KVObject, KVProperty, OBFactoryMap

from TG.helix.actors import HelixActor
from .node import MatuiNode
from .cell import MatuiCell

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SGMultiOp(KVObject):
    _fm_ = OBFactoryMap()

    _sgOps_ = []
    _sgOpMasks_ = []

    def sgBindNode(self, node):
        self.node = node

        for mask in self._sgOpMasks_:
            node.maskPass(mask)

        for op in self._sgOps_:
            node.addPassFrom(self, op)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Actor
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiActor(HelixActor, SGMultiOp):
    _fm_ = SGMultiOp._fm_.copy()
    _fm_.update(Node=MatuiNode, Cell=MatuiCell)
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

        self.sgBindNode(node)

        node.actor_ref = self.asStrongRef()
        def cleanup(wr, nr=node.asWeakRef()): 
            node = nr()
            if node is not None: 
                node.clear()
        self._wr_cleanup = self.asWeakRef(cleanup)


