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
from TG.metaObserving import obInstProperty

from TG.helix.actors import HelixActor
from TG.helix.actors import HelixStage

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpressResources(object):
    _partial = staticmethod(partial)
    def __init__(self, actor):
        pass
    def load(self, sgNode, sgo):
        pass

ExpressResources.property = classmethod(obInstProperty)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpressGraphOp(object):
    cullStack = False
    def __init__(self, actor, sgNode): 
        pass
    def bindPass(self, sgNode, sgo): 
        return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpressActor(HelixActor, KVObject):
    sceneGraphOps = {'render': None, 'resize': None}

    def __init__(self):
        self.kvpub.copyWithHost(self)

    def sceneGraphOpFor(self, sgOpKey, sgNode):
        sgOpFactory = self.sceneGraphOps[sgOpKey]
        if sgOpFactory is not None:
            return sgOpFactory(self, sgNode)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ExpressStage(HelixStage, KVObject):
    def onSceneSetup(self, scene):
        pass

    def onSceneShutdown(self, scene):
        pass

    def onSceneAnimate(self, scene, info):
        return True

