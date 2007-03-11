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

    def __init__(self, scene):
        self.scene = scene
        self.stage = scene.stage

        sceneMeter = getattr(scene, 'meter', None)
        if sceneMeter is not None:
            self.meter = sceneMeter

    _passResult = None
    _passVersion = None
    def sgPass(self):
        root = self.stage.node
        if self._passVersion is root.treeVersion:
            return self._passResult

        result = self._compileGraphPass(root)
        self._passResult = result
        self._passVersion = root.treeVersion
        return result

    def _compileGraphPass(self, root):
        graphPassOpsFrom = self._graphPassOpsFrom

        passUnwindStack = [] # a stack of unwind ops, which are lists themselves
        passResult = [] # a list of callables -- will eventuall contain all of the unwind stack

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
                    passUnwindStack.append([])
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphRenderPassManager(SceneGraphPassManager):
    resourceSelector = None 
    def _graphPassOpsFrom(self, node):
        actor = node.item
        if actor is None:
            return None

        resources = actor.resources
        if resources is None:
            return None

        passItem = resources.get(self.resourceSelector, None)
        if passItem is None:
            return None

        wind = passItem.bind(actor, resources, self)
        unwind = passItem.bindUnwind(actor, resources, self)
        return (wind, unwind, cullStack)

