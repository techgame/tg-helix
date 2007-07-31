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

    _passStackNames = ['passKey', 'result', 'info']

    def __init__(self, renderContext):
        self.renderContext = renderContext
        self.init()

    def init(self):
        self._passStack = []
        self.swapKeys = self.swapKeys.copy()
        self.debugCallTrees = self.debugCallTrees.copy()

    def _pushStackPass(self):
        items = dict((n, getattr(self, n)) for n in self._passStackNames)
        self._passStack.append(items)
    def _popStackPass(self):
        items = self._passStack.pop()
        for n, v in items.items():
            setattr(self, n, v)

    def startPass(self, sgpass, info):
        self._pushStackPass()

        self.passKey = sgpass.passKey
        self.info = info
        self.result = None

        rctx = self.renderContext
        rctx.select()

        self.vpsize = rctx.getSize()

    def finishPass(self, sgpass, info):
        result = self.result
        if sgpass.passKey in self.swapKeys:
            self.renderContext.swap()
            self.invalidated = False

        self._popStackPass()
        return result

    def invalidate(self):
        self.invalidated = True

