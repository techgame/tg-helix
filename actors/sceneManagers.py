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
    passItem = getattr(node, self.passItemKey, None)
    if passItem is None:
        return None, False

    wind, unwind = passItem.bindPass(node, self.sgo)
    return (wind, unwind), (hasChildren and passItem.cullStack)

def vectorDispatch(graphPassFns, sgo):
    # intended to be a replaceable method to call each method with a single
    # argument in a tight loop.
    for fn in graphPassFns:
        fn(sgo)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ResizeManager(SceneGraphPassManager):
    passItemKey = 'resizePass'
    graphPassItemsFrom = graphPassBoundFnsFrom
    walkGraph = staticmethod(vectorDispatch)
    sgo = property(lambda self: self)

    def resize(self, viewport, viewportSize):
        self.viewportSize = viewportSize

        viewport.setViewCurrent()
        
        mtoken = self.meter.start()
        self.walkGraph(self.graphPass(), self.sgo)
        self.meter.end(mtoken)

        return True
    __call__ = resize

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderManager(SceneGraphPassManager):
    passItemKey = 'renderPass'
    graphPassItemsFrom = graphPassBoundFnsFrom
    walkGraph = staticmethod(vectorDispatch)
    sgo = property(lambda self: self)

    def render(self, viewport):
        viewport.setViewCurrent()

        sgo = self.sgo

        mtoken = self.meter.start()
        self.walkGraph(self.graphPass(), self.sgo)
        self.meter.end(mtoken)

        viewport.viewSwapBuffers()
        return True
    __call__ = render

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LoadManager(RenderManager):
    passItemKey = 'loadPass'
    def graphPass(self):
        result = RenderManager.graphPass(self)

        # clear the graph pass cache until the next time it needs compiled
        self.graphPassCache = []
        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SelectManager(SceneGraphPassManager):
    passItemKey = 'selectPass'
    graphPassItemsFrom = graphPassBoundFnsFrom
    walkGraph = staticmethod(vectorDispatch)
    sgo = property(lambda self: self)

    debugView = False
    selectPos = (0,0)
    selectSize = (1,1)

    def select(self, viewport, pos):
        viewport.setViewCurrent()

        sgo = self.sgo

        self.selectPos = pos
        self.selection = []

        mtoken = self.meter.start()
        self.walkGraph(self.graphPass(), self.sgo)
        self.meter.end(mtoken)

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

