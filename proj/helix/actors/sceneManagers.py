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

from .sceneGraphPass import SceneGraphRenderPassManager

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewportResizeManager(SceneGraphRenderPassManager):
    resourceSelector = 'resize'

    def resize(self, viewport, viewportSize):
        self.viewportSize = viewportSize
        viewport.setViewCurrent()
        
        self.meter.start()
        sgpass = self.sgPass()
        for each in sgpass:
            each()
        self.meter.end()

        return True
    __call__ = resize

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderManager(SceneGraphRenderPassManager):
    resourceSelector = 'render'

    def render(self, viewport):
        viewport.setViewCurrent()

        self.meter.start()
        sgpass = self.sgPass()
        for each in sgpass:
            each()
        self.meter.end()

        viewport.viewSwapBuffers()
        return True
    __call__ = render

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SelectManager(SceneGraphRenderPassManager):
    resourceSelector = 'pick'

    debugView = False
    selectPos = (0,0)
    selectSize = (1,1)

    def select(self, viewport, pos):
        viewport.setViewCurrent()

        self.selectPos = pos
        self.selection = []

        self.meter.start()
        sgpass = self.sgPass()
        for each in sgpass:
            each()
        self.meter.end()

        if self.debugView:
            viewport.viewSwapBuffers()
            self.debugView = False

        return self.selection
    __call__ = select


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

