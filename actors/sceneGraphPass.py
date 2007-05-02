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

from TG.geomath.alg.graphPass import GraphPass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene managers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CallTree(object):
    def __init__(self, passKey):
        self.passKey = passKey

    def on(self, fn):
        self.add(fn)
        return fn
    def add(self, *fns):
        self._wind.extend(fns)

    def onUnwind(self, fn):
        self.addUnwind(fn)
        return fn
    def addUnwind(self, *fns):
        self._unwind.extend(fns)

    def cull(self, bCull=True):
        self._cull = bCull

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphPass(GraphPass):
    def __init__(self, node, passKey):
        self.node = node
        node.onTreeChange = self._node_onTreeRootChange
        self.passKey = passKey

    def _node_onTreeRootChange(self, rootNode, treeChanges=None):
        self._passList = None
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _passList = None
    def compile(self, sgo, passKey=None):
        result = self._passList
        if result is not None:
            return result

        if passKey is None:
            passKey = self.passKey

        ct = CallTree(passKey)
        ct._wind = []; ct._unwind = []; ct._stack = []

        itree = self.iterStack()
        for op, node in itree:
            ct._cull = False

            if op < 0:
                ct._wind.extend(ct._unwind)
                ct._wind.extend(ct._stack.pop())
                del ct._unwind[:]
                continue

            node.sgPassBind(ct, sgo)

            if op == 0 or ct._cull:
                ct._wind.extend(ct._unwind)
                del ct._unwind[:]

                if op > 0: itree.send(True)

            else: # op > 0
                ct._stack.append(ct._unwind)
                ct._unwind = []

        result = ct._wind
        assert not ct._unwind, ('Unwind list not empty:', self._unwind)
        assert not ct._stack, ('Unwind stack not empty:', self._stack)

        self._passList = result
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def perform(self, sgo):
        passlist = self.compile(sgo)
        for fn in passlist:
            fn(sgo)
    __call__ = perform

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphOnePass(SceneGraphPass):
    def perform(self, sgo):
        passlist = self.compile(sgo)
        if passlist:
            for fn in passlist:
                fn(sgo)
            self._passList = []
    __call__ = perform

