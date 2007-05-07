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

class SceneGraphCallTree(CallTree):
    def __init__(self, srm, passKey):
        self.srm = srm
        self.passKeyStack = [passKey]
        self.passKey = passKey

    _op_next = CallTree._op_
    def _op_(self, op, node, itree, compileNodeTo):
        self.ov.append('-^v'[op])
        self._op_next(op, node, itree, compileNodeTo)

    _compile_next = CallTree._compile_
    def _compile_(self, itree, compileNodeTo):
        self.ov = []
        r = self._compile_next(itree, compileNodeTo)

        ov = ''.join(self.ov)
        print '%10s = %s | %d ops %d fn' % (self.passKey, ov, len(ov), len(r))
        return r

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
        return node

    def newCallTree(self):
        return SceneGraphCallTree(self.srm, self.passKey)

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

    def performSubpass(self, info):
        passList = self.compile()
        self.perform(self.srm, passList)

