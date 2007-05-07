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

from TG.metaObserving import OBKeyedList, asWeakMethod
from TG.kvObserving import KVList
from TG.helix.actors import HelixNode

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Node
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiNode(HelixNode):
    actor_ref = None
    def __init__(self, **kw):
        for n,v in kw.items():
            setattr(self, n, v)

        self.bindPass = OBKeyedList()
        self._parents = KVList()
        self._children = KVList()

    def isLayout(self): return False

    def sgPassBind(self, ct):
        self.bindPass.call_n2(ct.passKey, self, ct)

    def onPass(self, passKey, fn=None, unwind=None):
        if fn is None:
            fn = passKey
            passKey = fn.__name__

            passKey = passKey.lstrip('sg_')
            if passKey.endswith('_unwind'):
                passKey = passKey.rstrip('_unwind')
                unwind = True

        fn = asWeakMethod(fn)

        if unwind: binder = lambda n, ct: ct.addUnwind(fn)
        else: binder = lambda n, ct: ct.add(fn)

        self.bindPass.add(passKey, binder)

    @classmethod
    def itemAsNode(klass, item, create=True):
        if item.isNode():
            return item
        return item._sgGetNode_(create)

    def onAddToParent(self, parent):
        r = HelixNode.onAddToParent(self, parent)

        if self.actor_ref is not None:
            actor = self.actor_ref()
            if actor is not None:
                self.actor_ref = actor.asStrongRef()
            else: 
                del self.actor_ref
        return r
    def onRemoveFromParent(self, parent):
        r = HelixNode.onRemoveFromParent(self, parent)
        
        if not self._parents:
            if self.actor_ref is not None:
                actor = self.actor_ref()
                if actor is not None:
                    self.actor_ref = actor.asWeakRef()
                else: 
                    del self.actor_ref
                    self.clear()
            else:
                self.clear()

        return r

