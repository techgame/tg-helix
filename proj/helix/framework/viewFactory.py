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

from TG.observing import ObservableTypeParticipant

from .visitor import IHelixVisitor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ View factory from visitType mechanism
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixViewFactory(IHelixVisitor):
    viewFactoryMap = None
    def __init__(self):
        self.viewFactoryMap = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def visitStage(self, stage):
        return self.createViewFor(stage, stage.allViewVisitKeys)
    def visitActor(self, actor):
        return self.createViewFor(actor, actor.allViewVisitKeys)
    def visitScene(self, scene):
        return scene
    def visitView(self, view):
        return view

    def __call__(self, item):
        return item.accept(self)

    def viewsFor(self, collection):
        for v in collection:
            yield v.accept(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createViewFor(self, viewable, viewKeys):
        viewFactory = self.getFactoryForKey(viewKeys)
        return viewFactory(viewable)

    def getFactoryForKey(self, viewKeys):
        viewFactoryMap = self.viewFactoryMap
        for key in viewKeys:
            viewFactory = viewFactoryMap.get(key, None)
            if viewFactory is not None:
                return viewFactory
        else:
            raise LookupError("Unable to find a viewFactory matching view keys: %r" % (viewKeys,))

    def addFactoryForKeys(self, viewFactory, allViewKeys):
        if not isinstance(allViewKeys, list):
            raise TypeError("allViewKeys must be a list of strings, but is a %r" % (allViewKeys.__class__, ))
        self.viewFactoryMap.update((key, viewFactory) for key in allViewKeys)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ View Factory Helpers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixViewFactoryBuilder(ObservableTypeParticipant):
    """This class helps to regiser view classes automatically as they are subclassed from HelixView"""
    def onObservableClassInit(self, selfAttrName, viewKlass):
        """Called when a subclass is created that has a reference to this
        factory in it's namespace"""
        viewKlass.viewFactoryRegister()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixViewFactoryMixin(object):
    ViewFactoryFactory = HelixViewFactory
    _viewFactory_builder_ = HelixViewFactoryBuilder()
    viewFactory = None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @staticmethod
    def registerViewFactory(klass, viewFactory=None):
        """Registeres a new view factory for a root view object.  Starts a new hierarchy of views for a certain namespace"""
        if klass.__subclasses__():
            raise RuntimeError("View factories must be registered before any subclasses are created")

        if viewFactory is None:
            viewFactory = klass.ViewFactoryFactory()
        klass.viewFactory = viewFactory
        
        klass.viewFactoryRegister()
        return viewFactory
    
    @classmethod
    def viewFactoryRegister(klass, viewKeys=None):
        """Registers this subclass with the viewFactory of the root view to handle viewKeys.  
        
        If viewKeys is None, the classes' viewFactoryKeys are used.
        (The root view is the nearest superclass that "registerViewFactory" was called on.)"""
        if viewKeys is None:
            viewKeys = klass.viewFactoryKeys()
        if viewKeys and klass.viewFactory:
            klass.viewFactory.addFactoryForKeys(klass.fromViewable, viewKeys)
            return True

    @classmethod
    def viewFactoryKeys(klass):
        """Returns the list of viewable keys this view can handle"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    @classmethod
    def fromViewable(klass, viewable):
        """Create an instance of the view for the viewable object"""
        raise NotImplementedError('Subclass Responsibility: %r, %r' % (klass, viewable))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Visit Types Mechanism
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixVisitTypesBuilder(ObservableTypeParticipant):
    """Compiles the actor visit types automatically as they are subclassed from HelixActor."""
    def onObservableClassInit(self, participantName, actorKlass):
        """Called when a subclass is created that has a reference to this
        factory in it's namespace"""
        actorKlass._buildVisitTypes()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixVisitTypeMixin(object):
    _visitTypes_builder_ = HelixVisitTypesBuilder()

    viewVisitKeys = []
    allViewVisitKeys = []

    @classmethod
    def _buildVisitTypes(klass):
        absent = object()

        allViewVisitKeys = [klass] + klass.viewVisitKeys
        for base in klass.__bases__:
            avvk = getattr(base, 'allViewVisitKeys', [])
            # skip the first entry -- should always be base, which the subclass
            # should not take over
            for vvk in avvk[1:]: 
                if vvk not in allViewVisitKeys:
                    allViewVisitKeys.append(vvk)

        klass.allViewVisitKeys = allViewVisitKeys

