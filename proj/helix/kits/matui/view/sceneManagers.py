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

from TG.openGL.layouts.absLayout import AbsLayoutStrategy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene managers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphPassManager(object):
    def __init__(self, scene):
        self.scene = scene
        self.root = scene.stage.node

    _passResult = None
    _passVersion = None
    def sgPass(self):
        root = self.root
        if self._passVersion is root.treeVersion:
            return self._passResult

        result = self._sgGeneratePass(root)
        self._passResult = result
        self._passVersion = root.treeVersion
        return result

    def _sgGeneratePass(self, root):
        addPassForNode = self._sgAddPassForNode

        result = self._sgNewPassResult()
        itree = root.iterTree()
        for op, node in itree:
            if op < 0: continue
            if addPassForNode(node, result):
                itree.send(True)
        return result

    def _sgNewPassResult(self):
        return []
    def _sgAddPassForNode(self, node, passResult):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LayoutManager(SceneGraphPassManager):
    strategy = AbsLayoutStrategy()
    box = Rect.property()

    def layout(self, glview):
        glview.setViewCurrent()

        cells = self.sgPass()
        self.strategy(cells, self.scene.box)

        return True

    def _sgAddPassForNode(self, node, cells):
        cellLayout = getattr(node.actor, 'layout', None)
        if cellLayout is not None:
            cells.append(cellLayout)
            return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Various Scene Graph Render Managers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewportResizeManager(SceneGraphPassManager):
    def resize(self, glview, viewportSize):
        self.viewportSize = viewportSize

        glview.setViewCurrent()
        sgpass = self.sgPass()
        for each in sgpass:
            each(self)

        return True

    def _sgAddPassForNode(self, node, passResult):
        actor = node.actor; resources = actor.resources
        resize = resources.get('resize', None)
        if resize is not None:
            passResult.append(resize.bind(actor, resources))
            return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderManager(SceneGraphPassManager):
    def render(self, glview):
        glview.setViewCurrent()
        glview.frameStart()

        sgpass = self.sgPass()
        for each in sgpass:
            each(self)

        glview.frameEnd()
        glview.viewSwapBuffers()
        return True

    def _sgAddPassForNode(self, node, passResult):
        actor = node.actor; resources = actor.resources
        render = resources.get('render', None)
        if render is not None:
            passResult.append(render.bind(actor, resources))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SelectManager(SceneGraphPassManager):
    def select(self, glview, pos):
        glview.setViewCurrent()

        sgpass = self.sgPass()
        for each in sgpass:
            each(self)

        return []

    def _sgAddPassForNode(self, node, passResult):
        actor = node.actor; resources = actor.resources
        render = resources.get('pick', None)
        if render is not None:
            passResult.append(render.bind(actor, resources))

