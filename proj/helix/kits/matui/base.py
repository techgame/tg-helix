##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.openGL.data import Rect

from TG.helix.framework.stage import HelixActor

from .node import MatuiNode
from .layouts import MatuiLayout

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiActor(HelixActor):
    viewVisitKeys = ['MatuiActor']

    box = Rect.property()
    minSize = None
    maxSize = None

    def isMatuiNode(self): return False
    def isMatuiActor(self): return True
    def isMatuiCell(self): return False
    def isMatuiLayout(self): return False

    def onCellLayout(self, cell, cbox):
        self.box.copyFrom(cbox)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    NodeFactory = MatuiNode.newNodeForActor
    def newNode(self, **kwinfo):
        node = self.NodeFactory(self)
        if kwinfo: 
            node.update(kwinfo)
        return node

    node = None
    def asNodeForHost(self, hostNode):
        node = self.node
        if node is None:
            node = self.newNode()
        return node

    def onNodeSetActor(self, node):
        if self.node is not None:
            raise RuntimeError("Actor already has a node")
        self.node = node

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    LayoutFactory = MatuiLayout.newLayoutForActor
    def newLayout(self, *args, **kw):
        layout = self.LayoutFactory(self, *args, **kw)
        return layout

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiStage(MatuiActor):
    viewVisitKeys = ["MatuiStage"]

    def isHelixStage(self):
        return True
    def accept(self, visitor):
        return visitor.visitStage(self)

    def loadForScene(self, scene):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

