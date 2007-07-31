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

from TG.geomath.data import DataHostObject, OBFactoryMap

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneRenderManager(DataHostObject):
    _fm_ = OBFactoryMap()
    invalidated = False
    passKey = None
    info = None
    result = None
    vpsize = (0,0)
    swapKeys = set(['render'])
    debugCallTrees = set([])

    def __init__(self, renderContext):
        self.renderContext = renderContext
        self.init()

    def init(self):
        self.swapKeys = self.swapKeys.copy()
        self.debugCallTrees = self.debugCallTrees.copy()

    def startPass(self, sgpass, info):
        if self.passKey is not None:
            raise RuntimeError("Already in pass '%s', cannot start pass '%s'" % (self.passKey, sgpass.passKey))
        self.passKey = sgpass.passKey
        rctx = self.renderContext
        rctx.select()

        self.info = info
        self.vpsize = rctx.getSize()
        self.result = None

    def finishPass(self, sgpass, info):
        result = self.result
        if sgpass.passKey in self.swapKeys:
            self.renderContext.swap()
            self.invalidated = False

        del self.result
        del self.info
        del self.passKey
        return result

    def invalidate(self):
        self.invalidated = True

