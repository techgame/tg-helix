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

from TG.observing import ObservableObject

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IHelixVisitor(ObservableObject):
    def visitScene(self, actor): pass
    def visitActor(self, actor): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixVisitor(IHelixVisitor):
    def visitActor(self, actor):
        return self._doGenericVisitActor(actor)
    def visitScene(self, actor):
        return self._doGenericVisitActor(actor)

    def _doGenericVisitActor(self, actor):
        actor, key, visit = self._findVisitActorByKeys(actor, actor.allVisitKeys)
        result = visit(actor)
        actor.acceptOnItems(self)
        return result

    def _findVisitActorByKeys(self, actor, allVisitKeys):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixMethodVisitor(HelixVisitor):
    def _findVisitActorByKeys(self, actor, allVisitKeys):
        for key in allVisitKeys:
            visit = getattr(self, 'onVisit'+key, None)
            if visit:
                return actor, key, visit
        else:
            return actor, None, self.onVisitNotFound

    def onVisitNotFound(self, actor):
        print '... no visit method for:', (actor, actor.allVisitKeys)

