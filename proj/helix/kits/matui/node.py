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

def printNodeTree(treeEntry, indent=0):
    node, children = treeEntry
    if not indent:
        print
        title = "Node Tree for: %r" % (node,)
        print title
        print "=" * len(title)

    print '%s- %r' % (' '*indent*2, node)

    indent += 1
    for ce in children:
        printNodeTree(ce, indent)
    indent -= 1

    if not indent:
        print
        print

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiNode(object):
    actor = None
    parent = None
    
    def __init__(self, actor=None, **kwinfo):
        self.info = {}

        self.children = []
        if actor is not None:
            self.setActor(actor)

        self.update(kwinfo)

    def __repr__(self):
        if self.actor is not None:
            return 'Node|%d|: %r' % (len(self), self.actor,)
        elif self.info is not None:
            return 'Node|%d|: {%r}' % (len(self), ', '.join(self.info.keys()),)
        else: return 'Node|%d|' % (len(self), )

    printNodeTree = staticmethod(printNodeTree)
    def debugTree(self):
        self.printNodeTree(self.tree())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def newNodeForActor(klass, actor):
        return klass(actor)

    def itemAsNode(self, item):
        isMatuiNode = getattr(item, 'isMatuiNode', lambda: False)
        if isMatuiNode():
            return item
        isMatuiActor = getattr(item, 'isMatuiActor', lambda: False)
        if isMatuiActor():
            return item.asNodeForHost(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def isMatuiNode(self): return True
    def isMatuiActor(self): return False
    def isMatuiCell(self): return False
    def isMatuiLayout(self): return False

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def accept(self, visitor):
        return visitor.visitNode(self)

    def update(self, info={}, **kwinfo):
        if info: self.info.update(info)
        if kwinfo: self.info.update(kwinfo)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _actor = None
    def getActor(self):
        return self._actor
    def setActor(self, actor):
        self._actor = actor
        if actor is not None:
            actor.onNodeSetActor(self)
    actor = property(getActor, setActor)

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
            return self, iter([])

        return (n for n in self.children if n.treeChanged)

    def tree(self, onlyChanged=False):
        if not onlyChanged:
            return self, (n.tree(onlyChanged) for n in self.children)
        elif self.treeChanged:
            return self, (n.tree(onlyChanged) for n in self.children if n.treeChanged)
        else: 
            return self, iter([])

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Node collection protocol
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __iadd__(self, other):
        self.add(other)
        return self
    def __isub__(self, other):
        self.remove(other)
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
        self.onTreeChange()

    # workhorses

    def insertNode(self, node, idx):
        if node.onAddToParent(self):
            self.children.insert(idx, node)
            self.onTreeChange()
            return node
    def addNode(self, node):
        if node.onAddToParent(self):
            self.children.append(node)
            self.onTreeChange()
            return node
    def removeNode(self, node):
        if node.onRemoveFromParent(self):
            self.children.remove(node)
            self.onTreeChange()
            return node

    def extendNodes(self, nodes):
        if nodes:
            for node in nodes:
                if node.onAddToParent(self):
                    self.children.append(node)
            self.onTreeChange()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onAddToParent(self, parent):
        oldParent = self.parent
        if oldParent is parent:
            return False
        if oldParent is not None:
            oldParent.removeNode(self)

        self.onTreeChange()
        self.parent = parent
        return True
        
    def onRemoveFromParent(self, parent):
        if parent is not self.parent:
            raise ValueError("Attempted to remove node from node that is not its parent")
            return False
        del self.parent
        self.onTreeChange()
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

