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
    treeChangeset = None # set(), created in flyweight()
    treeNodeTable = None # dict(), created in flyweight()

    parents = None
    children = None
    data = None
    
    def isNode(self): return True

    def __init__(self, data=None):
        self.parents = []
        self.children = []

        if data is not None:
            self.data = data
            self.treeNodeTable[data] = node

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def flyweight(klass):
        subklass = type(klass)(klass.__name__+'*', (klass,), dict(
            treeChangeset=set(),
            treeNodeTable=dict(),
            ))
        return subklass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Node and Node Tree  iteration
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def iterTree(self, depthFirst=True, nextLevelFor=(lambda cnode: cnode.children)):
        return (cnode for op, cnode in self.iterTreeStack(depthFirst, nextLevelFor) if op >= 0)
    def iterTreeStack(self, depthFirst=True, nextLevelFor=(lambda cnode: cnode.children)):
        stack = [(None, iter([self]))]

        while stack:
            if depthFirst:
                idx = len(stack)
            else: idx = 0
            ttree = stack[idx][1]

            for cnode in ttree:
                nextLevel = nextLevelFor(cnode)
                if nextLevel:
                    if (yield +1, cnode):
                        yield 'no-push'
                    else:
                        stack.append((cnode, iter(nextLevel)))
                        if depthFirst: break
                else: 
                    if (yield 0, cnode):
                        yield 'no-op'

            else:
                cnode = stack.pop(idx)[0]
                if cnode is not None:
                    if (yield -1, cnode):
                        yield 'no-op'
                
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

    def treeChanged(self):
        treeChangeset = self.treeChangeset
        if self in treeChangeset:
            # we are already changed
            return

        changeset = set([self])

        itree = root.iterParentTreeStack(False)
        for op, p in itree:
            if op >= 0:
                if p in changeset or p in treeChangeset:
                    # cull the depth first search iteration because this parent
                    # tree is already recorded in the changeset
                    itree.send(True) 
                else:
                    chaneset.add(p)

        treeChangeset.update(changeset)

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

    def __contains__(self, other):
        node = self.itemAsNode(other, False)
        return node in self.children
    def __iadd__(self, other):
        self.add(other)
        return self
    def __isub__(self, other):
        self.remove(other)
        return self

    def insert(self, idx, item):
        node = self.itemAsNode(item)
        if node.onAddToParent(self):
            self.children.insert(idx, node)
            self.treeChanged()
            return node

    def insertBefore(self, node, nidx):
        """Inserts node before index of nidx in children"""
        nidx = self.itemAsNode(nidx, False)
        idx = self.children.index(nidx)
        return self.insert(idx, node)
    def insertAfter(self, node, nidx):
        """Inserts node after index of nidx in children"""
        nidx = self.itemAsNode(nidx, False)
        idx = self.children.index(nidx) + 1
        return self.insert(idx, node)

    def add(self, item):
        node = self.itemAsNode(item)
        if node.onAddToParent(self):
            self.children.append(node)
            self.treeChanged()
            return node

    def extend(self, iterable):
        itemAsNode = self.itemAsNode
        children = self.children
        for each in iterable:
            node = itemAsNode(each)
            if node.onAddToParent(self):
                children.append(node)
        self.treeChanged()

    def remove(self, item):
        node = self.itemAsNode(item, False)
        if node is None: 
            return
        if node.onRemoveFromParent(self):
            while node in self.children:
                self.children.remove(node)
            self.treeChanged()
            return node

    def clear(self):
        nodeList = self.children[:]
        del self.children[:]

        for node in nodeList:
            node.onRemoveFromParent(self)
        self.treeChanged()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Node coersion
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def itemAsNode(self, item, create=True):
        if item.isNode():
            return item

        node = self.treeNodeTable.get(item, None)
        if node is None and create:
            node = item.asNodeWith(self.nodeFactory)
        return node

    @classmethod
    def nodeFactory(klass, data):
        return klass(data)

Node = HelixNode

