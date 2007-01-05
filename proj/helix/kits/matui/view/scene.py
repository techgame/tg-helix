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
from functools import partial

from TG.openGL.data import Rect
from TG.openGL.raw import gl

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
        self.box = stage.box
        stage.loadForScene(self)

    def update(self, stage):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setup(self, evtSources=[], **kwinfo):
        self.managers = {}
        self.setupManagers(self.managers)

        self.setupEvtSources(evtSources)

        self.stage.onSceneSetup(self)
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

    def layout(self, viewportSize):
        cells = self.sgLayoutCells()

        box = self.scene.box
        box.size = viewportSize
        self.strategy(cells, box)

        #if 0:
        #    self.scene.stage.node.debugTree()

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
    def render(self):
        renderList = self.sgRenderList()
        #if 0:
        #    print
        #    print "Render each:"
        #    self.glClearBuffers()
        #    for r in renderList:
        #        print '  ', r
        #    print
        #    return True
        self.glClearBuffers()
        for r in renderList:
            pass
        return True

    glClearBuffers = staticmethod(partial(gl.glClear, gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT))

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
    def select(self, pos):
        selectionList = self.sgSelectionList()
        #if 0:
        #    print
        #    print "Selectables:", pos
        #    for r in selectionList:
        #        print '  ', r
        #    print
        #    return

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

