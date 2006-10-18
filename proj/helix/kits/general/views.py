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

from TG.helix.framework.scene import HelixView
from TG.helix.framework.visitor import IHelixVisitor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Views 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderViewFactoryVisitor(IHelixVisitor):
    def visitScene(self, scene):
        return self.visitActor(scene)
    def visitActor(self, actor):
        viewFactoryMap = self.viewFactoryMap
        for key in actor.allVisitKeys:
            viewFactory = viewFactoryMap.get(key, None)
            if viewFactory is not None:
                return viewFactory(actor)
        else:
            return None

    viewFactoryMap = None
    def addViewForKeys(self, renderViewKlass, allViewKeys):
        viewFactoryMap = self.viewFactoryMap
        if viewFactoryMap is None:
            viewFactoryMap = {}
            self.viewFactoryMap = viewFactoryMap

        for key in allViewKeys:
            if key in viewFactoryMap:
                raise KeyError("Key %r already exists in viewFactoryMap")
            viewFactoryMap[key] = renderViewKlass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BuildVisitTypeViews(ObservableTypeParticipant):
    def onObservableClassInit(self, selfAttrName, renderViewKlass):
        viewFactory = renderViewKlass.viewFactory
        if viewFactory is not None:
            viewForKeys = self._getKeyList(renderViewKlass.viewForKeys)
            viewFactory.addViewForKeys(renderViewKlass, viewForKeys)

    def _getKeyList(self, e):
        if isinstance(e, (list, tuple)):
            return [k for i in e for k in self._getKeyList(i)]
        elif isinstance(e, basestring):
            return [e]
        elif isinstance(e, type):
            return getattr(e, 'allVisitKeys', [e.__name__])[:1]

        raise TypeError('Unable to determine key for view: %r' % (e,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BasicView(HelixView):
    _buildViews_ = BuildVisitTypeViews()
    viewFactory = RenderViewFactoryVisitor()
    viewForKeys = []

    def __init__(self, actor=None):
        self.init(actor)

    def init(self, actor):
        pass
    def resize(self, actor, size):
        pass
    def render(self, actor):
        pass

