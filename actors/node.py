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

    def sgPassBind(self, ct):
        pass

    def extendAt(self, idx, iterable):
        if isinstance(iterable, HelixObject):
            return self.insert(idx, iterable)

        return GraphNode.extendAt(self, idx, iterable)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _sgPassCache = None
    def asSGPassNode(self):
        if self._sgPassCache is not None:
            return self

        self._sgPassCache = {}
        self.onTreeChange = self._onPassTreeChange_
        return self

    srm = None
    def _onPassTreeChange_(self, node, cause=None):
        for p in self.iterParents():
            if p.srm is not None:
                p.srm.invalidate()
                
        self._sgPassCache.clear()
        return False

