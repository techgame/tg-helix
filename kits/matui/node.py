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

from TG.metaObserving import OBKeyedList
from TG.kvObserving import KVList
from TG.helix.actors import HelixNode

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Node
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiNode(HelixNode):
    def __init__(self, **kw):
        for n,v in kw.items():
            setattr(self, n, v)

        self.bindPass = OBKeyedList()
        self.parents = KVList()
        self.children = KVList()

    info = None
    actor = None
    def _getSubjectRepr(self):
        info = self.info
        if info: return self.info
        actor = self.actor
        if actor is None: 
            return '*'
        return actor.__class__.__name__

    def sgPassBind(self, ct):
        self.bindPass.call_n3(ct.passKey, self, ct, ct.srm)

    def isLayout(self): return False

    @classmethod
    def itemAsNode(klass, item, create=True):
        if item.isNode():
            return item
        return item._sgGetNode_(create)

