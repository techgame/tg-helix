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

class ScenePassMeter(object):
    def start(self): pass
    def end(self): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphPassManager(object):
    meter = ScenePassMeter()

    def __init__(self, scene):
        self.scene = scene
        self.stage = scene.stage

        sceneMeter = getattr(scene, 'meter', None)
        if sceneMeter is not None:
            self.meter = sceneMeter

    _passResult = None
    _passVersion = None
    def sgPass(self):
        root = self.stage.node
        if self._passVersion is root.treeVersion:
            return self._passResult

        result = self._sgGeneratePass(root)
        self._passResult = result
        self._passVersion = root.treeVersion
        return result

    def _sgGeneratePass(self, root):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def _handleException(self, err):
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphRenderPassManager(SceneGraphPassManager):
    resourceSelector = None 
    def _sgGeneratePass(self, root):
        resourceSelector = self.resourceSelector
        passResult = []
        passUnwindStack = []
        itree = root.iterTree()
        for op, node in itree:
            if op < 0: 
                passResult.extend(passUnwindStack.pop())
                node.treeChanged = False
                continue

            passItem = None
            actor = node.actor
            if actor is not None:
                resources = actor.resources
                if resources is not None:
                    passItem = resources.get(resourceSelector, None)

            if passItem is not None:
                wind = passItem.bind(actor, resources, self)
                unwind = passItem.bindUnwind(actor, resources, self)

                if op:
                    passResult.extend(wind)
                    if passItem.cullStack:
                        passResult.extend(unwind)
                        itree.send(True)
                    else:
                        # push our unwind stack
                        passUnwindStack.append(unwind)

                else: 
                    passResult.extend(wind)
                    passResult.extend(unwind)

            elif op > 0: 
                # push an empty unwind stack
                passUnwindStack.append([])

        assert not passUnwindStack, passUnwindStack
        return passResult

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewportResizeManager(SceneGraphRenderPassManager):
    resourceSelector = 'resize'

    def resize(self, hostView, viewportSize):
        self.viewportSize = viewportSize
        hostView.setViewCurrent()
        
        try:
            self.meter.start()
            sgpass = self.sgPass()
            for each in sgpass:
                each()
            self.meter.end()
        except Exception, err:
            if not self._handleException(err):
                raise

        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderManager(SceneGraphRenderPassManager):
    resourceSelector = 'render'

    def render(self, hostView):
        hostView.setViewCurrent()

        try:
            self.meter.start()
            sgpass = self.sgPass()
            for each in sgpass:
                each()
            self.meter.end()
        except Exception, err:
            if not self._handleException(err):
                raise

        hostView.viewSwapBuffers()
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SelectManager(SceneGraphRenderPassManager):
    resourceSelector = 'pick'

    debugView = False
    selectPos = (0,0)
    selectSize = (1,1)

    def select(self, hostView, pos):
        hostView.setViewCurrent()

        try:
            self.selectPos = pos
            self.selection = []

            self.meter.start()
            sgpass = self.sgPass()
            for each in sgpass:
                each()
            self.meter.end()
        except Exception, err:
            if not self._handleException(err):
                raise

        if self.debugView:
            hostView.viewSwapBuffers()
            self.debugView = False

        return self.selection

    def startSelector(self, selector):
        self.selector = selector
    def finishSelector(self, selector, selection):
        del self.selector
        self.selection += selection
    def setItem(self, item=None): 
        self.selector.setItem(item)
    def pushItem(self, item=None): 
        self.selector.pushItem(item)
    def popItem(self, item=None): 
        self.selector.popItem()

