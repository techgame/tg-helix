##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2007  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.ext.openGL.selection import NameSelector
from TG.helix.actors.sceneGraphPass import SceneGraphPass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PickNodeSceneGraphPass(SceneGraphPass):
    passKeyRender = 'render'

    _fm_ = SceneGraphPass._fm_.copy()
    _fm_.update(NameSelector = NameSelector)

    def compileNodeTo(self, cnode, ct):
        self.pushNodeOnNames(cnode, ct)

        # now bind 'render' passKey so the nodes can be selected
        passKey = ct.passKey
        ct.passKey = self.passKeyRender
        try:
            cnode.sgPassBind(ct)
        finally:
            ct.passKey = passKey

    def pushNodeOnNames(self, cnode, ct):
        if cnode is self.root:
            ct.add(self.sg_pickNode)
            cnode.sgPassBind(ct)
            ct.addUnwind(self.sg_pickNode_unwind)
        else:
            ct.add(lambda srm: srm.ns.push(cnode))
            cnode.sgPassBind(ct)
            ct.addUnwind(lambda srm: srm.ns.pop())

    def sg_pickNode(self, srm):
        srm.ns = self._fm_.NameSelector()
        srm.ns.start()
        srm.ns.push(self.root)

    def sg_pickNode_unwind(self, srm):
        srm.ns.pop()
        srm.result = srm.ns.finish()
        del srm.ns

        if srm.info.get('printTree', False):
            self.printSelectionTree(srm)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def printSelectionTree(self, srm):
        nodeSelection = srm.result

        print
        print 'All Nodes under cursor:'
        self.printTree(self.makeTreeFromSelection(nodeSelection))
        print

        print
        print 'Top Nodes under cursor:'
        self.printTree(self.makeTreeFromSelection(nodeSelection[-1:]))
        print

    @classmethod
    def printTree(klass, tree, lvl=0, indent='  '):
        for n, br in tree:
            print '%s%r' % (indent*lvl, n)
            if br:
                klass.printTree(br, lvl+1, indent)

    @staticmethod
    def makeTreeFromSelection(selection):
        tree = []
        for stack in selection:
            br = tree
            for i in stack:
                n = i[0]
                for e in br:
                    if e[0] is n:
                        br = e[1]
                        break
                else:
                    br.append((n, []))
                    br = br[-1][1]
        return tree

