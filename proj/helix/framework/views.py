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

from TG.observing import ObservableObject, ObservableTypeParticipant
from .visitor import IHelixVisitor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixViewFactory(IHelixVisitor):
    def visitStage(self, stage):
        return self.createViewFor(stage)
    def visitActor(self, actor):
        return self.createViewFor(actor, actor.allVisitKeys)
    def visitScene(self, scene):
        return self.createViewFor(scene)
    def visitView(self, view):
        return view

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createViewFor(self, viewable, viewKeys=None):
        if viewKeys is None:
            viewKeys = [viewable.__class__.__name__]
        viewFactory = self.getFactoryForKey(viewKeys)
        if viewFactory is not None:
            return viewFactory(viewable)

    viewFactoryMap = None
    def getFactoryForKey(self, viewKeys):
        viewFactoryMap = self.viewFactoryMap
        for key in viewKeys:
            viewFactory = viewFactoryMap.get(key, None)
            if viewFactory is not None:
                return viewFactory
        else:
            return None

    def addFactoryForKeys(self, viewFactory, allViewKeys):
        allViewKeys = self._getAllViewKeys(allViewKeys)
        viewFactoryMap = self.viewFactoryMap
        if viewFactoryMap is None:
            self.viewFactoryMap = viewFactoryMap = {}
        viewFactoryMap.update((key, viewFactory) for key in allViewKeys)

    def _getAllViewKeys(self, viewKeys):
        if isinstance(viewKeys, (list, tuple)):
            return [k for i in viewKeys for k in self._getAllViewKeys(i)]
        elif isinstance(viewKeys, basestring):
            return [viewKeys]
        elif isinstance(viewKeys, type):
            return getattr(viewKeys, 'allVisitKeys', [viewKeys.__name__])[:1]
        else:
            return list(viewKeys)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixViewFactoryBuilder(ObservableTypeParticipant):
    def onObservableClassInit(self, selfAttrName, viewKlass):
        """Called when a subclass is created that has a reference to this
        factory in it's namespace"""
        viewKlass._viewFactoryRegister()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixView(ObservableObject):
    _factory_builder_ = HelixViewFactoryBuilder()
    viewForKeys = []
    ViewFactoryFactory = HelixViewFactory
    viewFactory = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def isHelixView(self):
        return True

    def accept(self, visitor):
        return visitor.visitView(self)

    def acceptOnItems(self, visitor):
        pass

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def fromViewable(klass, viewable):
        raise NotImplementedError('Subclass Responsibility: %r, %r' % (klass, viewable))

    @staticmethod
    def registerViewFactory(klass, viewFactory=None):
        if klass.__subclasses__():
            raise RuntimeError("View factories must be registered before any subclasses are created")

        if viewFactory is None:
            viewFactory = klass.ViewFactoryFactory()
        klass.viewFactory = viewFactory
        
        klass._viewFactoryRegister()
        return viewFactory
    
    @classmethod
    def _viewFactoryKeys(klass):
        return klass.viewForKeys
    @classmethod
    def _viewFactoryRegister(klass):
        viewKeys = klass._viewFactoryKeys()
        if viewKeys and klass.viewFactory:
            klass.viewFactory.addFactoryForKeys(klass.fromViewable, viewKeys)
            return True

