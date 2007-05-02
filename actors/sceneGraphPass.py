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
    def add(self, *fns):
        self._wind.extend(fns)
    def addUnwind(self, *fns):
        self._unwind.extend(fns)
    def cull(self, bCull=True):
        self._cull = bCull

class SceneGraphPass(GraphPass):
    def __init__(self, node, passItemKey):
        self.node = node
        node.onTreeChange = self.onTreeRootChange
        self.passItemKey = passItemKey

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _passList = None
    def compile(self, sgo):
        result = self._passList
        if result is not None:
            return result

        ct = CallTree()
        ct._wind = []; ct._unwind = []; ct._stack = []

        itree = self.iterStack()
        for op, node in itree:
            ct._cull = False

            if op < 0:
                ct._wind.extend(ct._unwind)
                ct._wind.extend(ct._stack.pop())
                del ct._unwind[:]
                continue

            self.visitNode(ct, node, sgo)

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

    def visitNode(self, ct, node, sgo):
        passItem = getattr(node, self.passItemKey, None)
        if passItem is None:
            return
        passItem.bindPass(ct, node, sgo)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onTreeRootChange(self, rootNode, treeChanges):
        self._passList = None
        return True

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

