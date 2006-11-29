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

from .visitor import IHelixVisitor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ View factory from visitType mechanism
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixViewFactoryBuilder(ObservableTypeParticipant):
    """This class helps to regiser view classes automatically as they are subclassed from HelixView"""
    def onObservableClassInit(self, selfAttrName, viewKlass):
        """Called when a subclass is created that has a reference to this
        factory in it's namespace"""
        viewKlass._viewFactoryRegister()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixViewFactory(IHelixVisitor):
    def __call__(self, item):
        return item.accept(self)

    def visitStage(self, stage):
        return self.createViewFor(stage, stage.allVisitKeys)
    def visitActor(self, actor):
        return self.createViewFor(actor, actor.allVisitKeys)
    def visitScene(self, scene):
        return scene
    def visitView(self, view):
        return view

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def createViewFor(self, viewable, viewKeys=None):
        if viewKeys is None:
            viewKeys = [base.__name__ for base in viewable.__class__.__mro__]
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
        
        klass._viewFactoryRegister()
        return viewFactory
    
    @classmethod
    def _viewFactoryRegister(klass, viewKeys=None):
        """Registers this subclass with the viewFactory of the root view to handle viewKeys.  
        
        If viewKeys is None, the classes' viewFactoryKeys are used.
        (The root view is the nearest superclass that "registerViewFactory" was called on.)"""
        if viewKeys is None:
            viewKeys = klass._viewFactoryKeys()
        if viewKeys and klass.viewFactory:
            klass.viewFactory.addFactoryForKeys(klass.fromViewable, viewKeys)
            return True

    @classmethod
    def _viewFactoryKeys(klass):
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
    visitKind = None
    _visitTypes_builder_ = HelixVisitTypesBuilder()

    @classmethod
    def _buildVisitTypes(klass):
        allVisitKeys = [klass.__name__]
        for base in klass.__mro__:
            if base is Observable:
                # don't trace past Observable
                break

            vtList = base.visitKind
            if not vtList:
                vtList = [base.__name__]
            elif isinstance(vtList, basestring):
                vtList = [vtList]
            for vt in vtList:
                if vt not in allVisitKeys:
                    allVisitKeys.append(vt)

        klass.allVisitKeys = allVisitKeys

