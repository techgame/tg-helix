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
    def visitActor(self, actor): pass
    def visitStage(self, stage): pass
    def visitScene(self, scene): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixVisitor(IHelixVisitor):
    def visitActor(self, actor):
        return self._doGenericVisit(actor)
    def visitStage(self, stage):
        return self._doGenericVisit(stage)
    def visitScene(self, scene):
        return self._doGenericVisit(scene)

    def _doGenericVisit(self, actor):
        item, key, visit = self._findVisitByKeys(item, item.allVisitKeys)
        result = visit(item)
        item.acceptOnItems(self)
        return result

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

