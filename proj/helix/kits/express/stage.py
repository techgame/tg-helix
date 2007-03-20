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

from functools import partial

from TG.kvObserving import KVObject

from TG.helix.actors import HelixActor
from TG.helix.actors import HelixStage

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpressGraphOp(object):
    cullStack = False
    def __init__(self, actor): pass
    def bind(self, node, mgr): return []
    def bindUnwind(self, node, mgr): return []

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpressActor(HelixActor, KVObject):
    sceneGraphOps = {'render': None, 'resize': None}

    def __init__(self):
        self.kvpub.copyWithHost(self)
        self._createSGNodes()

    def _createSGNodes(self):
        # sgNodes is filled in by the scene graph node
        # constructors as a debugging courtesy 
        self.sgNodes = {}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpressStage(HelixStage, KVObject):
    def onSceneSetup(self, scene):
        pass

    def onSceneShutdown(self, scene):
        pass

    def onSceneAnimate(self, scene, info):
        return True

