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
    _passMask = set()

    def __init__(self, **kw):
        for n,v in kw.items():
            setattr(self, n, v)

        self._bindPass = OBKeyedList()
        self._parents = KVList()
        self._children = KVList()

    def isLayout(self): return False

    @classmethod
    def itemAsNode(klass, item, create=True):
        if item.isNode():
            return item
        return item._sgGetNode_(create)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _getPassRepr(self, sep=' '):
        return sep.join(sorted(self._bindPass.keys()))

    def sgPassBind(self, ct):
        self._bindPass.call_n2(ct.passKey, self, ct)

    def addPass(self, passKey, passBindFn, idx=None):
        if passKey in self._passMask:
            return None

        passAtKey = self._bindPass[passKey]
        if idx is None:
            passAtKey.append(passBindFn)
        else: passAtKey.insert(idx, passBindFn)

        self.sg_clearPassKey(passKey, False)
        return passBindFn

    def clearPass(self, passKey):
        self._bindPass.clear(passKey)
        self.sg_clearPassKey(passKey, False)

    def maskPass(self, passKey):
        mask = self._passMask or set()
        if passKey not in mask:
            mask.add(passKey)
            self._passMask = mask
            self.clearPass(passKey)

    def getPassBindFnFor(self, passKey, fn=None):
        if fn is None:
            fn = passKey
            passKey = fn.__name__
            if passKey.startswith('sg_'):
                passKey = passKey[3:]

        if passKey.endswith('_unwind'):
            passKey = passKey[:-7]
            unwind = True
        else: unwind = False

        if fn is None:
            return passKey, None

        fn = asWeakMethod(fn)
        if unwind: 
            passBindFn = lambda n, ct: ct.addUnwind(fn)
        else: 
            passBindFn = lambda n, ct: ct.add(fn)
        return passKey, passBindFn

    def onPass(self, passKey, fn=None, idx=None):
        passKey, passBindFn = self.getPassBindFnFor(passKey, fn)
        if passBindFn is not None:
            return self.addPass(passKey, passBindFn, idx)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Using onAdd/onRemove from parent events, Manage references
    # so that nodes and actors cleanup when they are no longer
    # referenced and no longer in the node tree 

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

