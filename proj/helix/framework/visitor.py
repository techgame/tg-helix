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
    def visitStage(self, stage): pass
    def visitActor(self, actor): pass
    def visitActorItems(self, actor): pass
    def visitScene(self, scene): pass
    def visitView(self, view): pass
    def visitViewItems(self, view): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixVisitor(IHelixVisitor):
    def visitAny(self, item):
        item, key, visit = self._findVisitByKeys(item, item.allVisitKeys)
        result = visit(item)
        item.acceptOnItems(self)
        return result

    visitStage = visitAny
    visitActor = visitAny
    visitScene = visitAny
    visitView = visitAny

    def _findVisitByKeys(self, item, allVisitKeys):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixMethodVisitor(HelixVisitor):
    def _findVisitByKeys(self, item, allVisitKeys):
        for key in allVisitKeys:
            visit = getattr(self, 'onVisit'+key, None)
            if visit:
                return item, key, visit
        else:
            return item, None, self.onVisitNotFound

    def onVisitNotFound(self, item):
        print '... no visit method for:', (item, item.allVisitKeys)

