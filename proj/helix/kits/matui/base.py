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

from TG.observing import ObservableObject
from . import node, layouts
from .resources import MatuiResources

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiActor(ObservableObject):
    def isMatuiNode(self): return False
    def isMatuiActor(self): return True
    def isMatuiCell(self): return False
    def isMatuiLayout(self): return False

    def __init__(self):
        self.initResources()

    def __repr__(self):
        pos = '%s %s' % tuple(self.box.pos.astype(int))
        size = '%s %s' % tuple(self.box.size.astype(int))
        return '<%s [%s %s]>' % (self.__class__.__name__, pos, size)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Actor Node protocol
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    NodeFactory = node.MatuiNode.newNodeForActor
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
    #~ Cell and Layout protocol
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    LayoutFactory = layouts.MatuiLayout.newLayoutForActor
    def newLayout(self, *args, **kw):
        layout = self.LayoutFactory(self, *args, **kw)
        return layout

    CellFactory = layouts.MatuiActorCell
    def newCell(self, *args, **kw):
        return self.CellFactory(self, *args, **kw)
    def asCellForHost(self, hostLayout):
        return self.newCell()

    def onCellLayout(self, cell, cbox):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Resource protocol
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    resources = MatuiResources()

    def initResources(self):
        resources = self.resources.forActor(self)
        self.resources = resources
        self.loadResources(resources)

    def loadResources(self, resources):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiStage(MatuiActor):
    NodeFactory = node.MatuiRootNode.newNodeForActor

    def loadForScene(self, scene):
        pass

    def onSceneSetup(self, scene):
        pass

    def onSceneAnimate(self, scene, hostView, info):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    resources = MatuiResources()
    resources.slot().stageMaterialGroup()
    box = None

