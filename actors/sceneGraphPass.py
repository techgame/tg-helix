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

from TG.geomath.alg.graphPass import CompiledGraphPass, CallTree

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene managers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphPass(CompiledGraphPass):
    def __init__(self, scene, passKey=None, singlePass=False):
        self.srm = scene.srm
        node = scene.root.newParent()
        CompiledGraphPass.__init__(self, node, passKey, singlePass)

    def newCallTree(self, passKey):
        ct = CallTree(passKey)
        ct.srm = self.srm
        return ct

    def compileNodeTo(self, node, ct):
        node.sgPassBind(ct, self.srm)

    def perform(self, info):
        passList = self.compile()
        if passList or not self.singlePass:
            return self.performPass(passList, info)
    __call__ = perform

    def performPass(self, passList, info):
        srm = self.srm
        srm.startPass(self, info)
        for fn in passList:
            fn(srm)
        return srm.finishPass(self, info)

