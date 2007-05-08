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

from . import base, node, events, sceneGraphPass, renderMgr

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneRenderContext(object):
    def getSize(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def select(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def swap(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixScene(base.HelixObject):
    """A Helix Scene is a mediator, tieing viewport, events, and managers together in an extensible way.
    
    The sgPass are called on by the events to handle rendering, resizing, and
    selection operations over the scene's nodes."""

    _fm_ = OBFactoryMap(
            Node = node.HelixNode,
            EventRoot = events.EventRoot,
            SceneRenderManager = renderMgr.SceneRenderManager,

            SGPass = sceneGraphPass.SceneGraphPass,
            SGPassEvents = OBKeyedList,
            )
    _sgPassTypes_ = []
    _sgPassTriggers_ = []

    def isScene(self): return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self):
        self.init()

    def init(self):
        self._sg_passes = {}
        self.root = self._fm_.Node(scene=self, info='SceneRoot')
        self.evtRoot = self._fm_.EventRoot()
        self.timestamp = self.evtRoot.newTimestamp

    def setup(self, renderContext):
        self.srm = self._fm_.SceneRenderManager(renderContext)
        self.root.srm = self.srm

        self.sgAddPasses(self._sgPassTypes_)
        self.sgPassConfig(self._sgPassTriggers_)
        self.setupEvtSources()
        return True

    def sgAddPasses(self, sgPassTypes):
        self.sgPassEvents = self._fm_.SGPassEvents()

        SGPass = self._fm_.SGPass
        root = self.root.asSGPassNode()
        for key, singlePass in sgPassTypes:
            self._sg_passes[key] = SGPass(self.root, key, singlePass)

    def sgPassConfig(self, sgPassTriggers):
        sg_passes = self._sg_passes
        sgPassEvents = self.sgPassEvents
        for passKey, preKeys, postKeys in sgPassTriggers:
            for dk in preKeys:
                dp = sg_passes.get(dk) 
                if dp is not None:
                    sgPassEvents.add(passKey+'-pre', dp.performSubpass)

            for dk in postKeys:
                dp = sg_passes.get(dk) 
                if dp is not None:
                    sgPassEvents.add(passKey+'-post', dp.performSubpass)

    def sg_pass(self, key, info=None):
        if info is None: 
            info = {}
        sgp = self._sg_passes[key]

        self.sgPassEvents.call_n1(key+'-pre', info)
        result = sgp(info, key)
        self.sgPassEvents.call_n1(key+'-post', info)
        return result

    def setupEvtSources(self):
        pass

