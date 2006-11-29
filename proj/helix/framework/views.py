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

from TG.observing import ObservableObject, ObservableTypeParticipant, ObservableList
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
    viewForKeys = []

    SubViewsFactory = HelixViewList

    def __init__(self):
        super(HelixView, self).__init__()
        self.init()

    def init(self):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def isHelixView(self):
        return True
    def accept(self, visitor):
        return visitor.visitView(self)
    def acceptOnItems(self, visitor):
        return visitor.visitViewItems(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def iterSubviewsFrom(klass, iterViewables):
        """Yiels views registerd to handle the items in the viewable iterator"""
        viewFactory = klass.viewFactory
        for viewable in iterViewables:
            yield viewFactory(viewable), viewable

    @classmethod
    def subviewsFrom(klass, iterViewables, subviews=None):
        """Creates views registerd to handle the items in the viewable iterator, and appends them to subviews"""
        if subviews is None:
            subviews = klass.SubViewsFactory()
        subviews.extend(self.iterSubviewsFrom(iterViewables)
        return subviews

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def _viewFactoryKeys(klass):
        """Returns the list of viewable keys this view can handle"""
        return klass.viewForKeys

    @classmethod
    def fromViewable(klass, viewable):
        """Create an instance of the view for the viewable object"""
        raise NotImplementedError('Subclass Responsibility: %r, %r' % (klass, viewable))

