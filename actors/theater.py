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

from TG.metaObserving import OBKeyedList
from TG.metaObserving import OBFactoryMap

from . import base
from .node import HelixNode
from .events import EventRoot
from .renderMgr import SceneRenderManager
from .sceneGraphPass import SceneGraphPass, SingleSceneGraphPass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TheaterRenderContext(object):
    def isRenderContext(self):
        return True
    def getSize(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def select(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def swap(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixTheater(base.HelixObject):
    """A Helix Theater is a mediator, tieing viewport, events, and managers together in an extensible way.
    
    The sgPass are called on by the events to handle rendering, resizing, and
    picking operations over the theater's nodes."""

    _fm_ = OBFactoryMap(
            Node = HelixNode,
            EventRoot = EventRoot,
            SceneRenderManager = SceneRenderManager,

            SGPassEvents = OBKeyedList,
            )
    _sgPassTypes_ = []
    _sgPassTriggers_ = []

    def isTheater(self): return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self):
        self.init()

    def init(self):
        self._sg_passes = {}
        self.root = self._fm_.Node(theater=self, info='SceneRoot')
        self.evtRoot = self._fm_.EventRoot(self.asWeakProxy())
        self.timestamp = self.evtRoot.newTimestamp

    def setup(self, renderContext):
        if not renderContext.isRenderContext():
            raise ValueError("renderContext must support TheaterRenderContext protocol")
        self.srm = self._fm_.SceneRenderManager(self, renderContext)

        self.sgAddPasses(self._sgPassTypes_)
        self.sgPassConfig(self._sgPassTriggers_)
        self.setupEvtSources()
        return True

    def sgAddPasses(self, sgPassTypes):
        self.sgPassEvents = self._fm_.SGPassEvents()

        root = self.root.asSGPassNode()
        for passKey, SGPassFactory in sgPassTypes:
            sgPass = SGPassFactory(self.root, passKey)
            self._sg_passes[passKey] = sgPass

    def sgPassConfig(self, sgPassTriggers):
        if not isinstance(sgPassTriggers, dict):
            sgPassTriggers = dict((key, (pre, post)) for key, pre, post in sgPassTriggers)
        self._sgPassTriggers_ = sgPassTriggers

    def sg_pass(self, key, info=None, sgPassInfo={}):
        if info is None: 
            info = {}

        sgPassInfo = dict(sgPassInfo)
        sgPassInfo.update(info=info, outerPassKey=key)

        result = None
        for sgKey, sgPass in self.iterSceneGraphPasses(key):
            spr = sgPass(sgPassInfo)
            if sgKey == key:
                result = spr
        return result

    def iterSceneGraphPasses(self, passListList=None):
        if passListList is None or isinstance(passListList, str):
            key = passListList
            passListList = list(self._sgPassTriggers_.get(key, []))
            passListList.insert(1, [key])

        sg_passes = self._sg_passes
        for passList in passListList:
            if isinstance(passList, str):
                passList = [passList]
            for passKey in passList:
                sgPass = sg_passes.get(passKey)
                if sgPass is not None:
                    yield passKey, sgPass

    def sg_invalidate(self):
        self.srm.invalidate()

    def setupEvtSources(self):
        pass

