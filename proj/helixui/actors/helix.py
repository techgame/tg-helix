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
