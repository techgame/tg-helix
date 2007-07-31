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

from TG.geomath.alg.graphNode import GraphNode
from .base import HelixObject

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixNode(GraphNode, HelixObject):
    def __init__(self, **kw):
        for n,v in kw.items():
            setattr(self, n, v)
        GraphNode.__init__(self)

    @classmethod
    def new(klass, **kw):
        return klass(**kw)

    def __repr__(self):
        r = [self._getSubjectRepr(), self._getPassRepr()]
        if r: r = ' ' + ' | '.join(r)
        else: r = ''
        return '<%s%s>' % (self.__class__.__name__, r)

    info = None
    def _getSubjectRepr(self):
        return self.info or '*%d' % (len(self._children),)
    def _getPassRepr(self, sep=' '):
        return None

    def extendAt(self, idx, iterable):
        if isinstance(iterable, HelixObject):
            return self.insert(idx, iterable)

        return GraphNode.extendAt(self, idx, iterable)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Scene graph management: passes and invalidation
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def sgPassBind(self, ct):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    theater = None
    def findTheater(self):
        for p in self.iterParents():
            if p.theater is not None:
                yield p.theater
                return

    def getSceneRenderManager(self):
        for theater in self.findTheater():
            return theater.srm
    srm = property(getSceneRenderManager)

    def sg_invalidate(self):
        srm = self.srm
        if srm is not None:
            srm.invalidate()
            return True
        else: return False

    sg_passCache = None
    def asSGPassNode(self):
        if self.sg_passCache is not None:
            return self

        self.sg_passCache = {}
        self.onTreeChange = self._onPassTreeChange_
        return self

    def _onPassTreeChange_(self, node, cause=None):
        self.sg_passCache.clear()
        self.sg_invalidate()
        return True

    def sg_clearPassKey(self, key, all):
        for p in self.iterParents():
            cache = p.sg_passCache
            if cache is not None:
                cache.pop(key, None)
                if not all: break

