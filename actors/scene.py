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
            )
    _sgPassTypes_ = []

    def isScene(self): return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self):
        self.init()

    def init(self):
        self._sg_passes = {}
        self.root = self._fm_.Node(scene=self, info='scene root')
        self.evtRoot = self._fm_.EventRoot()
        self.timestamp = self.evtRoot.newTimestamp

    def setup(self, renderContext):
        self.srm = self._fm_.SceneRenderManager(renderContext)
        self.sgAddPasses(self._sgPassTypes_)
        self.sgPassConfig(self._sg_passes)
        self.setupEvtSources()
        return True

    def sgAddPasses(self, sgPassTypes):
        SGPass = self._fm_.SGPass
        for key, singlePass in sgPassTypes:
            self._sg_passes[key] = SGPass(self, key, singlePass)

    def sgPassConfig(self):
        pass

    def sg_pass(self, key, info=None):
        if info is None: info = {}
        sgp = self._sg_passes[key]
        return sgp(info)

    def setupEvtSources(self):
        pass

