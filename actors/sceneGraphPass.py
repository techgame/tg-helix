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

class ScenePassMeter(object):
    def start(self): pass
    def end(self, token): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphPass(GraphPass):
    def __init__(self, node, passItemKey):
        self.node = node
        node.onTreeChange = self.onTreeRootChange
        self.passItemKey = passItemKey

    def onTreeRootChange(self, rootNode, treeChanges):
        return True

    def compile(self, sgo):
        emptyUnwind = [] # a "constant" empty list
        passUnwindStack = [] # a stack of unwind op lists
        passResult = [] # a linearized graph pass -- will eventually contain
                        # the wind ops and all of the unwind op stack in 
                        # correct traversal order

        itree = self.iterStack()
        for op, node in itree:
            if op < 0: 
                # a pop operation -- add the unwind stack top to our pass
                # result and continue the iteration
                passResult.extend(passUnwindStack.pop())
                continue
            pushUnwind = (op > 0)

            # get sgNodeItems fromm our node using template method
            sgNodeItems, cullStack = self.graphPassItemsFrom(sgo, node, pushUnwind)

            if pushUnwind and cullStack:
                itree.send(True)
                pushUnwind = False

            if sgNodeItems is None:
                if pushUnwind:
                    # push an empty unwind on the stack
                    passUnwindStack.append(emptyUnwind)
                continue

            # unpack sgNodeItems
            wind, unwind = sgNodeItems

            if wind:
                # wind ops go directly on the result
                passResult.extend(wind)

            # if we are pushing and not culling...
            if pushUnwind:
                # push the unwind ops on the stack
                passUnwindStack.append(unwind or emptyUnwind)
            elif unwind:
                # push(unwind); extend(pop) --> extend(unwind)
                passResult.extend(unwind)

        # make sure that all the pop operations came through to empty our unwind stack
        assert not passUnwindStack, passUnwindStack
        return passResult

    def perform(self, sgo):
        graphPassFns = self.compile(sgo)
        for fn in graphPassFns:
            fn(sgo)
    __call__ = perform

    def graphPassItemsFrom(self, sgo, node, hasChildren):
        passItem = getattr(node, self.passItemKey, None)
        if passItem is None:
            return None, False

        wind, unwind = passItem.bindPass(node, sgo)
        return (wind, unwind), (hasChildren and passItem.cullStack)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphPassEx(SceneGraphPass):
    _graphPassFns = None
    def onTreeRootChange(self, rootNode, treeChanges):
        self._graphPassFns = None
        return True

    def compile(self, sgo):
        r = self._graphPassFns
        if r is None:
            r = SceneGraphPass.compile(self, sgo)
            self._graphPassFns = r
        return r

