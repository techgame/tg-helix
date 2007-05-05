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

from TG.geomath.alg.compiledGraphPass import CompiledGraphPass, CallTree

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene managers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphPass(CompiledGraphPass):
    def __init__(self, scene, passKey=None, singlePass=False):
        if passKey is not None:
            self.passKey = passKey
        self.srm = scene.srm

        node = self._getNodeFromScene(scene)
        CompiledGraphPass.__init__(self, node, singlePass)

    def _getNodeFromScene(self, scene):
        node = scene.root.newParent()
        node.info = 'sgp:' + self.passKey
        node.pre = node.insertNew(0)
        node.pre.info = 'sgp:pre-'+self.passKey
        node.post = node.addNew()
        node.post.info = 'sgp:post-'+self.passKey
        return node

    def newCallTree(self):
        ct = CallTree()
        ct.srm = self.srm
        ct.passKey = self.passKey
        return ct

    def compileNodeTo(self, node, ct):
        node.sgPassBind(ct)

    def perform(self, srm, passList=None):
        if passList is None:
            passList = self.compile()

        for fn in passList:
            fn(srm)

    def performPass(self, info):
        passList = self.compile()
        if not passList and self.singlePass:
            return

        srm = self.srm
        srm.startPass(self, info)
        self.perform(srm, passList)
        return srm.finishPass(self, info)
    __call__ = performPass

