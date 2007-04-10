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

from functools import partial

from TG.kvObserving import KVObject, KVProperty
from TG.metaObserving import obInstProperty

from TG.helix.actors import HelixActor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Resources(object):
    partial = staticmethod(partial)
    def __init__(self, actor):
        pass
    def load(self, node, sgo):
        pass

Resources.property = classmethod(obInstProperty)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GraphOp(object):
    cullStack = False
    partial = staticmethod(partial)
    def __init__(self, actor, node): 
        pass
    def bindPass(self, node, sgo): 
        return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiActor(HelixActor, KVObject):
    _sgOps_ = {'render': None, 'resize': None, 'select': None}
    _sgNode_ = KVProperty(None)

    def __init__(self):
        self.kvpub.copyWithHost(self)

    def _sgNewNode_(self, nodeFactory, sgOpRequired):
        if self._sgNode_ is not None:
            raise RuntimeError("sgNewNode called multiple times for MatuiActor")

        node = nodeFactory()
        self._sgNode_ = node
        self._sgOpSetup_(node, sgOpRequired)
        return node

    def _sgOpSetup_(self, node, sgOpRequired):
        sgOpRequired = sgOpRequired.copy()

        for sgOpKey, sgOpFactory in self._sgOps_.items:
            if sgOpFactory is not None: 
                sgOp = sgOpFactory(self, node)
                sgOpRequired.pop(sgOpRequired, None)
                setattr(node, sgOpKey+'Pass', sgOp)

        for sgOpKey, sgOpDefault in sgOpRequired.items():
            sgOpKey += 'Pass'
            if sgOpDefault:
                setattr(node, sgOpKey, getattr(node, sgOpKey, None))
            else: setattr(node, sgOpKey, None)

