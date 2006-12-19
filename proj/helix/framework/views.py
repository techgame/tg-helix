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

from TG.observing import ObservableObject, ObservableList
from .viewFactory import HelixViewFactoryMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixViewList(ObservableList):
    def add(self, view):
        self.append(view)
        return view
    def accept(self, visitor):
        self.acceptOnItems(visitor)
    def acceptOnItems(self, visitor):
        for view in self:
            view.accept(visitor)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixView(ObservableObject, HelixViewFactoryMixin):
    ViewList = HelixViewList

    def isHelixView(self):
        return True
    def accept(self, visitor):
        return visitor.visitView(self)
    def acceptOnItems(self, visitor):
        return visitor.visitViewItems(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def viewListFor(klass, viewables, viewList=None):
        """Extends viewList with views registered to handle viewables"""
        if viewList is None:
            viewList = klass.ViewList()
        viewList.extend(klass.viewFactory.viewsFor(viewables))
        return viewList

