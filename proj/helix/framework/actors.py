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

from TG.observing import Observable, ObservableTypeParticipant, ObservableList

from TG.helix.geometry import geometry

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RebuildAllVisitTypes(ObservableTypeParticipant):
    def onObservableClassInit(self, participantName, observableKlass):
        self._rebuildAllVisitTypes(observableKlass)

    def _rebuildAllVisitTypes(self, klass):
        allVisitKeys = [klass.__name__]
        for base in klass.__mro__:
            if base is Observable:
                # don't trace past Observable
                break

            vt = base.visitKind
            if not vt:
                vt = base.__name__
            if vt not in allVisitKeys:
                allVisitKeys.append(vt)

        klass.allVisitKeys = allVisitKeys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixActorList(ObservableList):
    def add(self, actor):
        self.append(actor)
        return actor

    def accept(self, visitor):
        for actor in self:
            actor.accept(visitor)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixActor(Observable):
    """Base class for all helix actors"""

    allVisitKeys = None
    visitKind = "Actor"
    __rebuildAllVisitTypes = RebuildAllVisitTypes()

    items = None
    ItemsFactory = HelixActorList

    def __init__(self):
        super(HelixActor, self).__init__()
        self.init()

    def init(self):
        pass

    def accept(self, visitor):
        return visitor.visitActor(self)

    def acceptOnItems(self, visitor):
        items = self.items
        if items is not None:
            return items.accept(visitor)

