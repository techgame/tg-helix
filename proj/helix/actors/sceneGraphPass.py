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
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneGraphRenderPassManager(SceneGraphPassManager):
    resourceSelector = None 
    def _compileGraphPass(self, root):
        graphPassItemFrom = self._graphPassItemFrom
        resourceSelector = self.resourceSelector

        passResult = []
        passUnwindStack = []
        itree = root.iterTreeStack()
        for op, node in itree:
            if op < 0: 
                passResult.extend(passUnwindStack.pop())
                node.treeChanged = False
                continue

            passItem = graphPassItemFrom(node)
            if passItem is not None:
                wind = passItem.bind(actor, resources, self)
                unwind = passItem.bindUnwind(actor, resources, self)

                if op:
                    passResult.extend(wind)
                    if passItem.cullStack:
                        passResult.extend(unwind)
                        itree.send(True)
                    else:
                        # push our unwind stack
                        passUnwindStack.append(unwind)

                else: 
                    passResult.extend(wind)
                    passResult.extend(unwind)

            elif op > 0: 
                # push an empty unwind stack
                passUnwindStack.append([])

        assert not passUnwindStack, passUnwindStack
        return passResult

    def _graphPassItemFrom(self, node):
        actor = node.actor
        if actor is not None:
            resources = actor.resources
            if resources is not None:
                passItem = resources.get(resourceSelector, None)

