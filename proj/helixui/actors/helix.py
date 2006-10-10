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

from TG.observing import Observable, ObservableProperty

from TG.helixui.geometry import GeometryFactory

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _setupAllVisitTypes(klass):
    allVisitTypes = []
    for base in klass.__mro__:
        if base is Observable:
            break
        vt = base.visitType
        if not vt or vt in allVisitTypes:
            vt = base.__name__
        allVisitTypes.append(vt)
    klass.allVisitTypes = allVisitTypes

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixActor(Observable):
    """Base class for all helix actors"""

    allVisitTypes = None
    visitType = None

    geom = GeometryFactory()

    def __new__(klass, *args, **kw):
        if klass.allVisitTypes is None:
            _setupAllVisitTypes(klass)

        return Observable.__new__(klass, *args, **kw)

    def visit(self, action):
        return action.visitActor(self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixCompositeActor(HelixActor):
    """Composite base class for all helix actors"""

    def visit(self, action):
        return action.visitCompositeActor(self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixVisitor(Observable):
    def visitActorByVisitTypes(self, actor, allVisitTypes=None):
        if allVisitTypes is None:
            allVisitTypes = actor.allVisitTypes

        acceptActor = self.acceptActorByVisitType
        for visitType in actor.allVisitTypes:
            if acceptActor(actor, visitType):
                break

    def acceptActorByVisitType(self, actor, visitType):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def visitActor(self, actor):
        self.visitActorByVisitTypes(actor)

    def visitCompositeActor(self, actor):
        self.visitActorByVisitTypes(actor)

