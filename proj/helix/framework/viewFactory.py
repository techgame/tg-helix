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
    def visit(self, item):
        accept = getattr(item, 'accept', None)
        if accept is not None:
            return accept(self)
        elif isinstance(item, tuple):
            return self.createViewFor(item[0], item[1])
        else:
            return self.createViewFor(item, item.__class__.__mro__)
    __call__ = visit

    def viewsFor(self, collection):
        for item in collection:
            if item is not None:
                yield self.visit(item)

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

    def addFactoryForKeys(self, viewFactory, viewKeys):
        if not isinstance(viewKeys, list):
            raise TypeError("viewKeys must be a list, but is a %r" % (viewKeys.__class__, ))
        self.viewFactoryMap.update((key, viewFactory) for key in viewKeys)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ View Factory Helpers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixViewFactoryBuilder(ObservableTypeParticipant):
    """This class helps to regiser view classes automatically as they are subclassed from HelixView"""
    def onObservableClassInit(self, selfAttrName, viewKlass, tcinfo):
        """Called when a subclass is created that has a reference to this
        factory in it's namespace"""
        viewKlass.viewFactoryRegister()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def _getViewFactory_(): None
def _setViewFactory_(value):
    raise RuntimeError("viewFactory can only be set at class creation")

class HelixViewFactoryMixin(object):
    viewForKeys = []
    _viewFactory_builder_ = HelixViewFactoryBuilder()
    viewFactory = property(_getViewFactory_, _setViewFactory_)

    @classmethod
    def viewFactoryRegister(klass, viewKeys=None):
        """Registers this subclass with the viewFactory of the root view to handle viewKeys.  
        
        If viewKeys is None, the classes' viewForKeys is used.
        (The root view is the nearest superclass that "registerViewFactory" was called on.)"""
        if viewKeys is None:
            viewKeys = klass.viewForKeys
        if viewKeys and klass.viewFactory:
            klass.viewFactory.addFactoryForKeys(klass.fromViewable, viewKeys)
            return True

    @classmethod
    def fromViewable(klass, viewable):
        """Create an instance of the view for the viewable object"""
        raise NotImplementedError('Subclass Responsibility: %r, %r' % (klass, viewable))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Visit Types Mechanism
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixVisitTypesBuilder(ObservableTypeParticipant):
    """Compiles the actor visit types automatically as they are subclassed from HelixActor."""
    def onObservableClassInit(self, participantName, actorKlass, tcinfo):
        """Called when a subclass is created that has a reference to this
        factory in it's namespace"""
        actorKlass._buildVisitTypes()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixViewVisitTypeMixin(object):
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

