##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene managers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ScenePassMeter(object):
    def start(self): pass
    def end(self): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphPassManager(object):
    meter = ScenePassMeter()

    def __init__(self, scene, root):
        self.root = root
        sceneMeter = getattr(scene, 'meter', None)
        if sceneMeter is not None:
            self.meter = sceneMeter

    graphPassCache = []
    def graphPass(self):
        if self.root.treeChangeset:
            # there are changes... recompile the graph
            self.graphPassCache = self.compileGraphPass(self.root)
        return self.graphPassCache

    def compileGraphPass(self, root):
        graphPassOpsFrom = self._graphPassOpsFrom

        emptyUnwind = [] # a "constant" empty list
        passUnwindStack = [] # a stack of unwind op lists
        passResult = [] # a linearized graph pass -- will eventually contain
                        # the wind ops and all of the unwind op stack in 
                        # correct traversal order

        itree = root.iterTreeStack()
        for op, node in itree:
            if op < 0: 
                # a pop operation -- add the unwind stack top to our pass
                # result and continue the iteration
                passResult.extend(passUnwindStack.pop())
                continue

            # get passOps fromm our node using template method
            passOps = graphPassOpsFrom(node)
            if passOps is None:
                if op > 0:
                    # push an empty unwind on the stack
                    passUnwindStack.append(emptyUnwind)
                continue

            # unpack passOps
            wind, unwind, cullStack = passOps

            # wind ops go directly on the result
            passResult.extend(wind)

            # if we are pushing and not culling...
            if op and not cullStack:
                # push the unwind ops on the stack
                passUnwindStack.append(unwind)
            else:
                # otherwise, just add the unwind as the next operations on the stack
                passResult.extend(unwind)
                # and tell the tree walk to cull the DFS tree walk of the scene graph
                itree.send(True)

        # make sure that all the pop operations came through to empty our unwind stack
        assert not passUnwindStack, passUnwindStack
        return passResult

    def _graphPassOpsFrom(self, node):
        passItem = node.item
        if passItem is None:
            return None

        wind = passItem.bind(actor, resources, self)
        unwind = passItem.bindUnwind(actor, resources, self)
        return (wind, unwind, cullStack)

