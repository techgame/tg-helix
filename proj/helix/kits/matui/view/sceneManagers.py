##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

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
    def layout(self, hostView):
        hostView.setViewCurrent()

        box = self.scene.stage.box
        sgpass = self.sgPass()
        for layout in sgpass:
            layout(box)

        return True

    resourceSelector = 'layout'
    def _sgGeneratePass(self, root):
        resourceSelector = self.resourceSelector

        layouts = []
        itree = root.iterTree()
        for op, node in itree:
            if op < 0: continue

            actor = node.actor; resources = actor.resources
            cellLayout = resources.get(resourceSelector, None)
            if cellLayout is not None:
                layouts.append(cellLayout)
                itree.send(True)

        return layouts

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Various Scene Graph Render Managers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphRenderPassManager(SceneGraphPassManager):
    resourceSelector = None 
    def _sgGeneratePass(self, root):
        resourceSelector = self.resourceSelector
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

                if not op or material.cullStack:
                    itree.send(True)
                    passResult.extend(reversed(passStack.pop()))

        assert not passStack, passStack
        return passResult


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewportResizeManager(SceneGraphRenderPassManager):
    resourceSelector = 'resize'

    def resize(self, hostView, viewportSize):
        self.viewportSize = viewportSize

        hostView.setViewCurrent()
        sgpass = self.sgPass()
        for each in sgpass:
            each()

        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderManager(SceneGraphRenderPassManager):
    resourceSelector = 'render'

    def render(self, hostView):
        hostView.setViewCurrent()
        hostView.frameStart()

        sgpass = self.sgPass()
        for each in sgpass:
            each()

        hostView.frameEnd()
        hostView.viewSwapBuffers()
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SelectManager(SceneGraphRenderPassManager):
    resourceSelector = 'pick'

    selectPos = (0,0)
    selectSize = (0,0)

    def select(self, hostView, pos):
        hostView.setViewCurrent()

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

