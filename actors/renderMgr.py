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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneRenderManager(object):
    invalidated = False
    info = None
    result = None
    vpsize = (0,0)
    swapKeys = set(['render'])

    def __init__(self, renderContext):
        self.renderContext = renderContext
        self.debugCallTrees = set()

    def startPass(self, sgpass, info):
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
        return result

    def invalidate(self):
        self.invalidated = invalidated
