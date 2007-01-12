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
    parents = None
    
    def __init__(self, actor=None, **kwinfo):
        self.info = {}

        self.parents = []
        self.children = []
        if actor is not None:
            self.setActor(actor)

        self.update(kwinfo)

    def __repr__(self):
        if self.actor is not None:
            if self.children:
                return 'Node|%d|: %r' % (len(self.children), self.actor,)
            else: return 'Node: %r' % (self.actor,)
        elif self.info is not None:
            return 'Node|%d|: {%r}' % (len(self.children), ', '.join(self.info.keys()),)
        else: return 'Node|%d|' % (len(self.children), )

    printNodeTree = staticmethod(printNodeTree)
    def debugTree(self):
        print
        title = "Node Tree for: %r" % (self,)
        print title
        print "=" * len(title)

        indent = 0
        for op, node in self.iterTree(): 
            if op >= 0:
                print '%s- %r' % (2*indent*' ', node)
            indent += op

        print
        print

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
        while root.parents:
            root = root.parents[0]
        return root
    def linage(self):
        return list(self.iterLinage())
    def iterLinage(self):
        each = self
        while each is not None:
            yield each
            each = each.parents[0]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __iter__(self):
        return iter(self.children)

    def iter(self):
        return iter(self.children)
    def iterChanged(self):
        if not self.treeChanged:
            return self, iter([])

        return (n for n in self.children if n.treeChanged)

    def iterTree(self):
        stack = [(None, iter([self]))]

        while stack:
            ttree = stack[-1][1]

            for cnode in ttree:
                if cnode.children:
                    if (yield +1, cnode):
                        yield 'no-push'
                    else:
                        stack.append((cnode, iter(cnode.children)))
                        break
                else: 
                    if (yield 0, cnode):
                        yield 'no-op'

            else:
                cnode = stack.pop()[0]
                if cnode is not None:
                    if (yield -1, cnode):
                        yield 'no-op'
                

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
        if item is None: return
        isMatuiNode = getattr(item, 'isMatuiNode', lambda: False)
        if isMatuiNode():
            return self.removeNode(item)
        node = getattr(item, 'node', None)
        if node is not None:
            return self.removeNode(node)

        for each in item:
            self.remove(each)

    def clear(self):
        return self.clearNodes()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def insertNodeBefore(self, node, nidx):
        """Inserts node before index of nidx in children"""
        idx = self.children.index(nidx)
        return self.insertNode(idx, node)
    def insertNodeAfter(self, node, nidx):
        """Inserts node after index of nidx in children"""
        idx = self.children.index(nidx) + 1
        return self.insertNode(idx, node)

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
            while node in self.children:
                self.children.remove(node)
            self.onTreeChange()
            return node
    def extendNodes(self, nodes):
        if nodes:
            for node in nodes:
                if node.onAddToParent(self):
                    self.children.append(node)
            self.onTreeChange()
    def clearNodes(self):
        nodeList = self.children[:]
        del self.children[:]

        for node in nodeList:
            node.onRemoveFromParent(self)
        self.onTreeChange()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def onAddToParent(self, parent):
        if parent not in self.parents:
            self.parents.append(parent)
        return True
        
    def onRemoveFromParent(self, parent):
        while parent in self.parents:
            self.parents.remove(parent)
        return True

    treeChanged = False
    def onTreeChange(self):
        if self.treeChanged:
            # we are already changed
            return

        self.treeChanged = True

        for p in self.parents:
            p.onTreeChange()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiRootNode(MatuiNode):
    treeVersion = 0
    def onTreeChange(self):
        if self.treeChanged:
            return

        self.treeVersion += 1

        if self.parents:
            # root nodes don't generally have parents, but just in case someone
            # wants to hijack it... ;)
            for p in self.parents:
                p.onTreeChange()

