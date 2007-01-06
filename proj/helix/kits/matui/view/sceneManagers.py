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

    def _sgGeneratePass(self, root):
        cells = []
        itree = root.iterTree()
        for op, node in itree:
            if op < 0: continue

            cellLayout = getattr(node.actor, 'layout', None)
            if cellLayout is not None:
                cells.append(cellLayout)
                itree.send(True)

        return cells

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Various Scene Graph Render Managers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphRenderPassManager(SceneGraphPassManager):
    resourceSelector = None 
    resourceFirstOnly = False
    def _sgGeneratePass(self, root):
        resourceSelector = self.resourceSelector
        resourceFirstOnly = self.resourceFirstOnly
        passResult = []
        passStack = []
        itree = root.iterTree()
        for op, node in itree:
            if op < 0: 
                passResult.extend(reversed(passStack.pop()))
                continue
            elif op > 0: 
                passStack.append([])

            actor = node.actor; resources = actor.resources
            material = resources.get(resourceSelector, None)
            if material is not None:
                passResult += material.bind(actor, resources, self)
                passStack[-1] += material.bindUnwind(actor, resources, self)

                if op and resourceFirstOnly:
                    itree.send(True)
                    passResult.extend(reversed(passStack.pop()))

        assert not passStack, passStack
        return passResult


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewportResizeManager(SceneGraphRenderPassManager):
    resourceSelector = 'resize'
    resourceFirstOnly = True

    def resize(self, glview, viewportSize):
        self.viewportSize = viewportSize

        glview.setViewCurrent()
        sgpass = self.sgPass()
        for each in sgpass:
            each()

        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderManager(SceneGraphRenderPassManager):
    resourceSelector = 'render'

    def render(self, glview):
        glview.setViewCurrent()
        glview.frameStart()

        sgpass = self.sgPass()
        for each in sgpass:
            each()

        glview.frameEnd()
        glview.viewSwapBuffers()
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SelectManager(SceneGraphRenderPassManager):
    resourceSelector = 'pick'

    selectPos = (0,0)
    selectSize = (0,0)

    def select(self, glview, pos):
        glview.setViewCurrent()

        self.selectPos = pos
        self.selection = []

        sgpass = self.sgPass()
        for each in sgpass:
            each()

        return self.selection

    def startSelector(self, selector):
        self.setItem = selector.setItem
        self.pushItem = selector.pushItem
        self.popItem = selector.popItem
    def finishSelector(self, selector, selection):
        self.selection += selection
        del self.setItem
        del self.pushItem
        del self.popItem

    def setItem(self, item):
        raise NotImplementedError('Selector Responsibility: %r' % (self,))
    def pushItem(self, item):
        raise NotImplementedError('Selector Responsibility: %r' % (self,))
    def popItem(self):
        raise NotImplementedError('Selector Responsibility: %r' % (self,))

