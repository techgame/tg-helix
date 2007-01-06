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
        self.updateResources(stage.resources.forView(self))

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

    def performLayout(self, glview, size):
        layoutMgr = self.managers['layout']
        layoutMgr.layout(size)
        return True

    def performRender(self, glview):
        glview.setViewCurrent()
        renderMgr = self.managers['render']
        glview.frameStart()
        if renderMgr.render():
            glview.frameEnd()
            glview.viewSwapBuffers()
            return True

    def performSelect(self, glview, pos):
        selectMgr = self.managers['select']
        return selectMgr.select(pos)

    def performAnimation(self, glview, info):
        if 0:
            self.performRender(glview)

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

    def layout(self, size):
        cells = self.sgLayoutCells()

        box = self.scene.box
        box.size = size
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
    def render(self):
        renderList = self.sgRenderList()

        self.glClearBuffers()
        for each in renderList:
            each.sgRender(self)
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
        for each in selectionList:
            each.sgSelect(self)

    selectionList = None
    treeVersion = None
    def sgSelectionList(self):
        root = self.scene.stage.node
        if self.treeVersion >= root.treeVersion:
            return self.selectionList

        viewForActor = self.scene.viewFactory

        selectionList = []
        itree = root.iterTree()
        for op, node in itree:
            if op >= 0:
                view = viewForActor(node.actor)
                if view is not None:
                    selectionList.append(view)

        self.treeVersion = root.treeVersion
        self.selectionList = selectionList
        return selectionList

