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

from pprint import pprint
from TG.openGL.data import Rect

from .base import MatuiView
from .events import MatuiEventRoot

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiScene(MatuiView):
    viewForKeys = ['MatuiStage']

    def __repr__(self):
        return '%s: %r' % (self.__class__.__name__, self.stage)

    def isHelixScene(self):
        return True
    def accept(self, visitor):
        return visitor.visitScene(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stage = None
    def init(self, stage):
        self.stage = stage
        stage.loadForScene(self)

    def update(self, stage):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setup(self, evtSources=[], **kwinfo):
        self.managers = {}
        self.setupManagers(self.managers)

        self.setupEvtSources(evtSources)
        return True

    def shutdown(self):
        return True

    evtRoot = MatuiEventRoot.property()
    def setupEvtSources(self, evtSources=[]):
        self.evtRoot.configFor(self, evtSources)

    def setupManagers(self, managers):
        managers.update(
            render=RenderManager(self),
            layout=LayoutManager(self),
            select=SelectionManager(self),
            )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene managers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneManagerBase(object):
    def __init__(self, scene):
        self.scene = scene

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.openGL.layouts.absLayout import AbsLayoutStrategy
class LayoutManager(SceneManagerBase):
    strategy = AbsLayoutStrategy()
    box = Rect.property()

    def __call__(self, viewportSize):
        cells = self.sgLayoutCells()

        box = self.box
        box.size = viewportSize
        self.strategy(cells, box)

    cells = None
    treeVersion = None
    def sgLayoutCells(self):
        root = self.scene.stage.node
        if self.treeVersion >= root.treeVersion:
            return self.cells

        cells = []
        itree = root.iterTree()
        for op, node in itree:
            if op >= 0:
                cellLayout = getattr(node.actor, 'layout', None)
                if cellLayout is not None:
                    cells.append(cellLayout)
                    itree.send(True)

        self.treeVersion = root.treeVersion
        self.cells = cells
        return cells

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderManager(SceneManagerBase):
    def __call__(self):
        renderList = self.sgRenderList()
        if 0:
            print
            print "Render each:"
            for r in renderList:
                print '  ', r
            print
        else:
            for r in renderList:
                pass
        return True

    renderList = None
    treeVersion = None
    def sgRenderList(self):
        root = self.scene.stage.node
        if self.treeVersion >= root.treeVersion:
            return self.renderList

        viewForActor = self.scene.viewFactory

        renderList = []
        itree = root.iterTree()
        for op, node in itree:
            if op >= 0:
                view = viewForActor(node.actor)
                if view is not None:
                    renderList.append(view)

        self.treeVersion = root.treeVersion
        self.renderList = renderList
        return renderList

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SelectionManager(SceneManagerBase):
    def __call__(self, pos):
        selectionList = self.sgSelectionList()
        if 0:
            print
            print "Selectables:", pos
            for r in selectionList:
                print '  ', r
            print
        else:
            for r in selectionList:
                pass

    selectionList = None
    treeVersion = None
    def sgSelectionList(self):
        root = self.scene.stage.node
        if self.treeVersion >= root.treeVersion:
            return self.selectionList

        selectionList = []
        itree = root.iterTree()
        for op, node in itree:
            if op >= 0:
                actor = node.actor
                if actor is not None:
                    selectionList.append(actor)

        self.treeVersion = root.treeVersion
        self.selectionList = selectionList
        return selectionList

