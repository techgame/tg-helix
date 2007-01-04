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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiNode(object):
    actor = None
    parent = None
    
    def __init__(self, actor=None):
        self.info = {}

        self.children = []
        if actor is not None:
            self.actor = actor

        self.update(actor, info, **kwinfo)

    @classmethod
    def newNodeForActor(klass, actor):
        return klass(actor)

    @classmethod
    def itemAsNode(klass, item):
        isMatuiNode = getattr(item, 'isMatuiNode', lambda: False)
        if isMatuiNode():
            return item
        isMatuiActor = getattr(item, 'isMatuiActor', lambda: False)
        if isMatuiActor():
            return klass.newNodeForActor(item)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def isMatuiNode(self):
        return True
    def isMatuiActor(self):
        return False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def accept(self, visitor):
        return visitor.visitMatuiNode(self)

    def update(self, info={}, **kwinfo):
        if info: self.info.update(info)
        if kwinfo: self.info.update(kwinfo)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Node and Node Tree  iteration
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def root(self):
        root = self
        while root.parent is not None:
            root = root.parent
        return root
    def linage(self):
        return list(self.iterLinage())
    def iterLinage(self):
        each = self
        while each is not None:
            yield each
            each = each.parent

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __len__(self):
        return len(self.children)
    def __iter__(self):
        return iter(self.children)

    def iter(self):
        return iter(self.children)
    def iterChanged(self):
        if not self.treeChanged:
            return iter([])
        return n for n in self.children if n.treeChanged

    def iterTree(self):
        return (n, n.iterTree()) for n in self.children
    def iterChangedTree(self, clear=False):
        if not self.treeChanged:
            return iter([])
        if clear: self.treeChanged = False
        return (n, n.iterChangedTree(clear)) for n in self.children if n.treeChanged

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Node collection protocol
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __iadd__(self, other):
        self.add(other):
        return self
    def __isub__(self, other):
        self.remove(other):
        return self

    def insert(self, idx, item):
        node = self.itemAsNode(item)

        if node is None:
            for each in item:
                self.insert(idx, each)
                idx += 1 # advance the index as we add items
            return self

        return self.insertNode(idx, node)

    def add(self, item):
        node = self.itemAsNode(item)

        if node is None:
            for each in item:
                self.add(each)
            return self

        return self.addNode(node)

    def remove(self, item):
        isMatuiNode = getattr(item, 'isMatuiNode', lambda: False)
        if isMatuiNode():
            return self.removeNode(item)

        for each in item:
            self.remove(each)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def insertNodeBefore(self, node, nidx):
        """Inserts node before index of nidx in children"""
        idx = self.children.index(nidx)
        return self.insertNode(idx, node)
    def insertNodeAfter(self, node, nidx):
        """Inserts node after index of nidx in children"""
        idx = self.children.index(nidx) + 1
        return self.insertNode(idx, node)

    def clearNodes(self):
        nodeList = self.children[:]
        del self.children[:]

        for node in nodeList:
            node.onRemoveFromParent(self)

    # workhorses

    def insertNode(self, node, idx):
        if node.onAddToParent(self):
            self.children.insert(idx, node)
            node.parent = self
            self.onTreeChange()
            return node
    def addNode(self, node):
        if node.onAddToParent(self):
            self.children.append(node)
            node.parent = self
            self.onTreeChange()
            return node
    def removeNode(self, node):
        if node.onRemoveFromParent(self):
            self.children.remove(node)
            del node.parent
            self.onTreeChange()
            return node

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onAddToParent(self, parent):
        oldParent = self.parent
        if oldParent is parent:
            return False
        if oldParent is not None:
            oldParent.removeNode(self)
        return True
        
    def onRemoveFromParent(self, parent):
        if parent is not self.parent:
            raise ValueError("Attempted to remove node from node that is not its parent")
            return False
        return True

    treeChanged = False
    def onTreeChange(self, notifyTree=True):
        if self.treeChanged:
            # we are already changed
            return True

        self.treeChanged = True

        if notifyTree:
            l = self.parent
            while l:
                if l.onTreeChange(False):
                    # this parent is changed, all its parents are changed
                    break
                l = l.parent
            return True

