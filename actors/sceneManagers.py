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

from .sceneGraphPass import SceneGraphPass, SceneGraphPassEx

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ScenePassMeter(object):
    def start(self): pass
    def end(self, token): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BaseManager(object):
    SGPassFactory = SceneGraphPassEx

    meter = ScenePassMeter()
    sgo = property(lambda self: self)

    def __init__(self, scene, root):
        self.sgPass = self.SGPassFactory(root, self.passItemKey)

        sceneMeter = getattr(scene, 'meter', None)
        if sceneMeter is not None:
            self.meter = sceneMeter

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ResizeManager(BaseManager):
    passItemKey = 'resizePass'

    def resize(self, viewport, viewportSize):
        self.viewportSize = viewportSize

        viewport.setViewCurrent()
        
        mtoken = self.meter.start()
        self.sgPass(self.sgo)
        self.meter.end(mtoken)

        return True
    __call__ = resize

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderManager(BaseManager):
    passItemKey = 'renderPass'

    def render(self, viewport):
        viewport.setViewCurrent()

        mtoken = self.meter.start()
        self.sgPass(self.sgo)
        self.meter.end(mtoken)

        viewport.viewSwapBuffers()
        return True
    __call__ = render

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LoadManager(RenderManager):
    SGPassFactory = SceneGraphPass
    passItemKey = 'loadPass'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SelectManager(BaseManager):
    passItemKey = 'selectPass'

    debugView = False
    selectPos = (0,0)
    selectSize = (1,1)

    def select(self, viewport, pos):
        viewport.setViewCurrent()

        self.selectPos = pos
        self.selection = []

        mtoken = self.meter.start()
        self.sgPass(self.sgo)
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

