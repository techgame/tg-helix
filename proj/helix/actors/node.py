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

from .base import HelixObject

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixNode(HelixObject):
    parents = None
    children = None
    
    def isNode(self): return True

    def __init__(self):
        self.parents = []
        self.children = []

    @classmethod
    def new(klass):
        return klass()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def flyweight(klass, **kwdata):
        return type(klass)(klass.__name__+'*', (klass,), kwdata)

    @classmethod
    def createRootForScene(klass, scene):
        rootKlass = klass.flyweight(scene=scene)
        return rootKlass()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Node coersion
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def itemAsNode(klass, item, create=True):
        """Override to provide conversion and creation utilities"""
        if item.isNode():
            return item

        node = None 
        if node is None and create:
            raise ValueError("Expected a HelixNode, but received %r" % (item.__class__,))

        return node

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Node and Node Tree  iteration
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def iterTree(self, depthFirst=True, nextLevelFor=(lambda cnode: cnode.children)):
        return (cnode for op, cnode in self.iterTreeStack(depthFirst, nextLevelFor) if op >= 0)
    def iterTreeStack(self, depthFirst=True, nextLevelFor=(lambda cnode: cnode.children)):
        stack = [(None, iter([self]))]

        while stack:
            if depthFirst:
                idx = len(stack) -1
            else: idx = 0
            ttree = stack[idx][1]

            for cnode in ttree:
                nextLevel = nextLevelFor(cnode)
                if nextLevel:
                    if (yield +1, cnode):
                        yield 'cull'
                    else:
                        stack.append((cnode, iter(nextLevel)))
                        if depthFirst: break
                else: 
                    if (yield 0, cnode):
                        yield 'noop'

            else:
                cnode = stack.pop(idx)[0]
                if cnode is not None:
                    if (yield -1, cnode):
                        yield 'noop'
                
    def iterParentTree(self, depthFirst=True, nextLevelFor=lambda cnode: cnode.parents):
        return (cnode for op, cnode in self.iterTreeStack(depthFirst, nextLevelFor) if op >= 0)
    def iterParentTreeStack(self, depthFirst=True, nextLevelFor=lambda cnode: cnode.parents):
        return self.iterTreeStack(depthFirst, nextLevelFor)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def debugTree(self, indent=0, indentStr='  ', nextLevelFor=lambda cnode: cnode.children):
        print
        title = "Node Tree for: %r" % (self,)
        print title
        print "=" * len(title)

        for op, node in self.iterTreeStack(True, nextLevelFor): 
            if op >= 0:
                print '%s- %r' % (indent*indentStr, node)
            indent += op

        print
        print

    def debugParentTree(self, indent=0, indentStr='  ', nextLevelFor=lambda cnode: cnode.parents):
        return self.debugTree(indent, indentStr, nextLevelFor)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Graph Change Recording
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    onTreeChange = None #onTreeChange(node, changeStack)
    def treeChanged(self, changeStack=None):
        visited = set()
        changeStack = changeStack or []

        itree = self.iterParentTreeStack(False)
        for op, node in itree:
            if op < 0: 
                changeStack.pop()
                continue
            elif node in visited:
                itree.send(True)
                continue

            visited.add(node)
            onTreeChange = node.onTreeChange
            if onTreeChange is not None:
                onTreeChange(node, changeStack)

            if op > 0:
                changeStack.append(node)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Parents collection
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onAddToParent(self, parent):
        if parent not in self.parents:
            self.parents.append(parent)
        return True
        
    def onRemoveFromParent(self, parent):
        while parent in self.parents:
            self.parents.remove(parent)
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Children collection
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return iter(self.children)

    def __getitem__(self, idx):
        return self.children[idx]
    def __delitem__(self, idx):
        nodeList = self.children[idx]
        del self.children[nodeList]
        self._removeNodeList(children)

    def __contains__(self, other):
        node = self.itemAsNode(other, False)
        return node in self.children

    def __iadd__(self, other):
        self.add(other)
        return self
    def __isub__(self, other):
        self.remove(other)
        return self

    def insertNew(self, idx):
        return self.insert(idx, self.new())
    def insert(self, idx, item):
        node = self.itemAsNode(item)
        if node.onAddToParent(self):
            self.children.insert(idx, node)
            self.treeChanged([node])
            return node

    def insertBefore(self, item, nidx):
        """Inserts item before index of nidx in children"""
        nidx = self.itemAsNode(nidx, False)
        idx = self.children.index(nidx)
        return self.insert(idx, item)
    def insertAfter(self, item, nidx):
        """Inserts item after index of nidx in children"""
        nidx = self.itemAsNode(nidx, False)
        idx = self.children.index(nidx) + 1
        return self.insert(idx, item)

    def addNew(self):
        return self.add(self.new())
    def add(self, item):
        node = self.itemAsNode(item)
        if node.onAddToParent(self):
            self.children.append(node)
            self.treeChanged([node])
            return node
    append = add

    def extend(self, iterable):
        itemAsNode = self.itemAsNode
        children = self.children

        nodeChanges = set()
        for each in iterable:
            node = itemAsNode(each)
            if node.onAddToParent(self):
                children.append(node)
                nodeChanges.add(node)
        self.treeChanged([nodeChanges])

    def remove(self, item):
        node = self.itemAsNode(item, False)
        if node is None: 
            return
        if node.onRemoveFromParent(self):
            self.children.remove(node)
            self.treeChanged([node])
            return node

    def clear(self):
        nodeList = self.children[:]
        del self.children[:]
        self._removeNodeList(nodeList)

    def _removeNodeList(self, nodeList):
        if not isinstance(nodeList, list):
            nodeList = [nodeList]
        nodeChanges = set()
        for node in nodeList:
            if node.onRemoveFromParent(self):
                nodeChanges.add(node)
        self.treeChanged([nodeChanges])

Node = HelixNode

