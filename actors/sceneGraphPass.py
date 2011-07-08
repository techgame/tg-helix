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

from TG.geomath.data import DataHostObject, OBFactoryMap
from TG.geomath.alg.compiledGraphPass import CompiledGraphPass, CompileCallStack

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene managers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphCallTree(CompileCallStack):
    def __init__(self, passKey, root):
        self.passKey = passKey
        self.root = root

class DebugSceneGraphCallTree(SceneGraphCallTree):
    _pop_next = SceneGraphCallTree._pop_
    def _pop_(self, op, cnode):
        self.ov.append('v')
        return self._pop_next(op, cnode)

    _step_next = SceneGraphCallTree._step_
    def _step_(self, op, cnode):
        self.ov.append('-^'[op])
        return self._step_next(op, cnode)

    _compile_next = SceneGraphCallTree._compile_
    def _compile_(self, itree, compileNodeTo):
        self.ov = []
        r = self._compile_next(itree, compileNodeTo)

        ov = ''.join(self.ov)
        nl = getattr(self.root, 'theater', None) is not None
        if nl: print
        print '%30s:%8s %2d/%2d | %s' % (self.root._getSubjectRepr(), self.passKey, len(r), len(ov), ov)
        return r

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphNodePass(CompiledGraphPass, DataHostObject):
    singlePass = False
    _fm_ = OBFactoryMap(
        SGCallTree = SceneGraphCallTree,
        SGDebugCallTree = DebugSceneGraphCallTree,
        )

    def newCompileStack(self, passKey, root):
        return self._fm_.SGCallTree(passKey, root)

    def _getCached(self, key, root):
        return root.sg_passCache.get(key, None)
    def _setCached(self, key, root, result):
        if self.singlePass:
            root.sg_passCache[key] = []
        else: root.sg_passCache[key] = result

    def compileNodeTo(self, op, cnode, ctree):
        cache = cnode.sg_passCache
        if cache is None or cnode is ctree.root:
            # compile the node to this pass
            return cnode.sgPassBind(ctree)

        # add a method to call the pre-cached subpass
        if cache.get(ctree.passKey, True):
            ctree.addFn(self.sg_pass, ctree.passKey, cnode)
        ctree.cull()

    def sg_pass(self, passKey, root, srm):
        passList = self.compile(passKey, root)
        self.performPassOnList(passList, srm)

    def performPassOnList(self, passList, srm):
        for fn in passList:
            fn(srm)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphPass(SceneGraphNodePass):
    def __init__(self, root, passKey):
        self.passKey = passKey

        SceneGraphNodePass.__init__(self, root)
        self.debugCallTrees = self.root.srm.debugCallTrees

    def newCompileStack(self, passKey, root):
        if passKey in self.debugCallTrees:
            return self._fm_.SGDebugCallTree(passKey, root)
        return self._fm_.SGCallTree(passKey, root)

    def performPass(self, sgPassInfo, passKey=None):
        if passKey is None:
            passKey = self.passKey

        sgPassInfo['passKey'] = passKey

        srm = self.root.srm
        srm.startPass(self, sgPassInfo)

        passList = self.compile(passKey)
        self.performPassOnList(passList, srm)

        return srm.finishPass(self, sgPassInfo)
    __call__ = performPass

class SingleSceneGraphPass(SceneGraphPass):
    singlePass = True

class EventSceneGraphPass(SceneGraphPass):
    def performPassOnList(self, passList, srm):
        for fn in passList:
            r = fn(srm)
            if r:
                return r

