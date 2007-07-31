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

from functools import partial
from TG.geomath.data import DataHostObject, OBFactoryMap
from TG.geomath.alg.compiledGraphPass import CompiledGraphPass, CompileStack

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene managers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphCallTree(CompileStack):
    def __init__(self, root, passKey):
        self.root = root
        self.passKey = passKey

    def addFn(self, fn, *args):
        if args:
            fn = partial(fn, *args)
        self._result.append(fn)
    def addUnwindFn(self, fn, *args):
        if args:
            fn = partial(fn, *args)
        self._unwind.append(fn)

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
        return self._fm_.SGCallTree(root, passKey)

    def _getCached(self, key, root):
        return root.sg_passCache.get(key, None)
    def _setCached(self, key, root, result):
        if self.singlePass:
            root.sg_passCache[key] = []
        else: root.sg_passCache[key] = result

    def compileNodeTo(self, cnode, ct):
        cache = cnode.sg_passCache
        if cache is None or cnode is ct.root:
            return cnode.sgPassBind(ct)

        if cache.get(ct.passKey, True):
            ct.addFn(self.sg_pass, ct.passKey, cnode)
        ct.cull()

    def sg_pass(self, passKey, root, srm):
        passList = self.compile(passKey, root)
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
            return self._fm_.SGDebugCallTree(root, passKey)
        return self._fm_.SGCallTree(root, passKey)

    def performPass(self, info, passKey=None):
        if passKey is None:
            passKey = self.passKey

        srm = self.root.srm
        srm.startPass(self, info)

        passList = self.compile(passKey)
        self.performPassOnList(passList, srm)

        return srm.finishPass(self, info)
    __call__ = performPass

    def performPassOnList(self, passList, srm):
        for fn in passList:
            fn(srm)

class SingleSceneGraphPass(SceneGraphPass):
    singlePass = True

class EventSceneGraphPass(SceneGraphPass):
    def performPassOnList(self, passList, srm):
        for fn in passList:
            r = fn(srm)
            if r:
                return r

