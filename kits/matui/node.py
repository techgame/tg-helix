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

from TG.metaObserving import OBKeyedList, asWeakMethod, OBFactoryMap
from TG.kvObserving import KVList
from TG.helix.actors import HelixNode

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Node
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiNode(HelixNode):
    _fm_ = OBFactoryMap(sgOpPrefix='sg_')
    actor_ref = None
    sgPassMask = set()

    def __init__(self, **kw):
        for n,v in kw.items():
            setattr(self, n, v)

        self.sgPassMask = self.sgPassMask.copy()
        self.sgPassChannels = OBKeyedList()
        self._parents = KVList()
        self._children = KVList()

    def isLayout(self): return False

    @classmethod
    def itemAsNode(klass, item, create=True):
        if item.isNode():
            return item
        return item._sgGetNode_(create)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Pass Management                                   
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _getPassRepr(self, sep=' '):
        return sep.join(sorted(self.sgPassChannels.keys()))

    def sgIsPassBound(self, passKey):
        return ((passKey not in self.sgPassMask)
            and (self.sgPassChannels.get(passKey)))

    def sgPassBind(self, ct):
        passKey = ct.passKey
        if passKey not in self.sgPassMask:
            self.sgPassChannels.call_n2(passKey, self, ct)

    def addPassRaw(self, passKey, passBindFn, idx=None):
        passAtKey = self.sgPassChannels[passKey]
        if idx is None:
            passAtKey.append(passBindFn)
        else: passAtKey.insert(idx, passBindFn)

        self.sg_rebuildPass(passKey, passKey=='load')
        return passBindFn

    def discardPassRaw(self, passKey, passBindFn):
        passAtKey = self.sgPassChannels[passKey]
        try:
            passAtKey.remove(passBindFn)
        except ValueError:
            return None
        else:
            self.sg_rebuildPass(passKey, False)
            return passBindFn

    def clearPass(self, passKey):
        self.sgPassChannels.clear(passKey)
        self.sg_rebuildPass(passKey, False)

    def maskPass(self, passKey, masked=True):
        sgPassMask = self.sgPassMask
        if masked:
            if passKey not in sgPassMask:
                sgPassMask.add(passKey)
        elif passKey in sgPassMask:
            sgPassMask.discard(passKey)

    def addPass(self, passKey, fn=None, idx=None):
        passKey, passBindFn = self._getPassBindFnFor(passKey, fn)
        if passBindFn is not None:
            return self.addPassRaw(passKey, passBindFn, idx)
    onPass = addPass

    def addPassFrom(self, host, opKey, opBind=None):
        if opBind is None:
            if isinstance(opKey, str):
                opBind = self._fm_.sgOpPrefix + opKey
            else: opKey, opBind = opKey

        if isinstance(opBind, str):
            opBind = getattr(host, opBind, None)

        if opBind is not None:
            idx = getattr(opBind, 'idx', None)
            self.onPass(opKey, opBind, idx=idx)
            return True
        else:
            return False

    def _getPassBindFnFor(self, passKey, fn=None):
        if fn is None:
            fn = passKey
            passKey = fn.__name__
            if passKey.startswith(self._fm_.sgOpPrefix):
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

        self.sg_rebuildPass('load', True)
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

