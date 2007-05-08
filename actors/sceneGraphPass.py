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
        nl = getattr(self.root, 'scene', None) is not None
        if nl: print
        print '%30s:%8s %2d/%2d | %s' % (self.root._getSubjectRepr(), self.passKey, len(r), len(ov), ov)
        return r

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphNodePass(CompiledGraphPass):
    singlePass = False
    if 0: SGCallTree = SceneGraphCallTree
    else: SGCallTree = DebugSceneGraphCallTree

    def newCompileStack(self, passKey, root):
        return self.SGCallTree(root, passKey)

    def _getCached(self, key, root):
        return root._sgPassCache.get(key, None)
    def _setCached(self, key, root, result):
        if self.singlePass:
            root._sgPassCache[key] = []
        else: root._sgPassCache[key] = result

    def compileNodeTo(self, cnode, ct):
        cache = cnode._sgPassCache
        if cache is None or cnode is ct.root:
            return cnode.sgPassBind(ct)

        ct.addFn(self.sg_pass, ct.passKey, cnode)
        ct.cull()

    def sg_pass(self, passKey, root, srm):
        passList = self.compile(passKey, root)
        for fn in passList:
            fn(srm)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphPass(SceneGraphNodePass):
    def __init__(self, root, passKey, singlePass):
        self.passKey = passKey
        if singlePass:
            self.singlePass = singlePass
        SceneGraphNodePass.__init__(self, root)

    def performSubpass(self, info, passKey=None):
        if passKey is None: 
            passKey = self.passKey

        srm = self.root.srm

        passList = self.compile(passKey)
        for fn in passList:
            fn(srm)

    def performPass(self, info, passKey=None):
        if passKey is None:
            passKey = self.passKey

        srm = self.root.srm
        srm.startPass(self, info)

        passList = self.compile(passKey)
        for fn in passList:
            fn(srm)

        return srm.finishPass(self, info)
    __call__ = performPass

