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

from TG.helix.framework.visitor import IHelixVisitor
from TG.helix.framework.actors import HelixActor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Views 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixView(ObservableObject):
    pass

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
        viewHost = renderViewKlass.viewHost
        if viewHost is not None:
            viewForKeys = [self._getViewForKeyAsString(e) for e in renderViewKlass.viewForKeys]
            viewHost.addViewForKeys(renderViewKlass, viewForKeys)

    def _getViewForKeyAsString(self, e):
        if isinstance(e, type) and issubclass(e, HelixActor):
            return e.allVisitKeys[0]
        else:
            return str(e)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderView(HelixView):
    _buildViews_ = BuildVisitTypeViews()
    viewHost = RenderViewFactoryVisitor()
    viewForKeys = []

    def __init__(self, actor):
        pass
    def resize(self, actor, size):
        pass
    def render(self, actor):
        pass

