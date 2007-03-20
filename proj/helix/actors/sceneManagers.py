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

from .sceneGraphPass import SceneGraphPassManager

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def graphPassBoundFnsFrom(self, node, hasChildren):
    passItem = node.item
    if passItem is None:
        return None, False

    wind, unwind = passItem.bindPass(node, self.sgo)
    return (wind, unwind), (hasChildren and passItem.cullStack)

class ResizeManager(SceneGraphPassManager):
    graphPassItemsFrom = graphPassBoundFnsFrom
    sgo = property(lambda self: self)

    def resize(self, viewport, viewportSize):
        self.viewportSize = viewportSize
        self.viewportAspect = viewportSize[0].__truediv__(viewportSize[1])

        viewport.setViewCurrent()
        
        sgo = self.sgo

        self.meter.start()
        graphPassFns = self.graphPass()
        for sgnFn in graphPassFns:
            sgnFn(sgo)
        self.meter.end()

        return True
    __call__ = resize

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderManager(SceneGraphPassManager):
    graphPassItemsFrom = graphPassBoundFnsFrom
    sgo = property(lambda self: self)

    def render(self, viewport):
        viewport.setViewCurrent()

        sgo = self.sgo

        self.meter.start()
        graphPassFns = self.graphPass()
        for sgnFn in graphPassFns:
            sgnFn(sgo)
        self.meter.end()

        viewport.viewSwapBuffers()
        return True
    __call__ = render

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SelectManager(SceneGraphPassManager):
    graphPassItemsFrom = graphPassBoundFnsFrom
    sgo = property(lambda self: self)

    debugView = False
    selectPos = (0,0)
    selectSize = (1,1)

    def select(self, viewport, pos):
        viewport.setViewCurrent()

        sgo = self.sgo

        self.selectPos = pos
        self.selection = []

        self.meter.start()
        graphPassFns = self.graphPass()
        for sgnFn in graphPassFns:
            sgnFn(sgo)
        self.meter.end()

        if self.debugView:
            viewport.viewSwapBuffers()
            self.debugView = False

        return self.selection
    __call__ = select

    # these operations may be called by the graphOps.  Reference to the manager
    # may be obtained during the compileGraphPass() operation
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

