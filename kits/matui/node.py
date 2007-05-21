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

        self._bindPass = OBKeyedList()
        self._parents = KVList()
        self._children = KVList()

    def isLayout(self): return False

    def _getPassRepr(self, sep=' '):
        return sep.join(sorted(self._bindPass.keys()))

    def sgPassBind(self, ct):
        self._bindPass.call_n2(ct.passKey, self, ct)

    def addPass(self, passKey, passBindFn):
        self._bindPass.add(passKey, passBindFn)
        self.sg_clearPassKey(passKey, False)
        return passBindFn

    def clearPass(self, passKey):
        self._bindPass.clear(passKey)
        self.sg_clearPassKey(passKey, False)

    def onPass(self, passKey, fn=None):
        if fn is None:
            fn = passKey
            passKey = fn.__name__
            if passKey.startswith('sg_'):
                passKey = passKey[3:]

        if passKey.endswith('_unwind'):
            passKey = passKey[:-7]
            unwind = True
        else: unwind = False

        fn = asWeakMethod(fn)

        if unwind: 
            passBindFn = lambda n, ct: ct.addUnwind(fn)
        else: 
            passBindFn = lambda n, ct: ct.add(fn)

        return self.addPass(passKey, passBindFn)

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

        self.sg_clearPassKey('load', True)
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

