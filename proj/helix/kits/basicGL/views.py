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

from TG.helixui.framework.scene import HelixView
from TG.helixui.framework.visitor import IHelixVisitor
from TG.helixui.framework.actors import HelixActor

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

        if isinstance(e, basestring):
            return [e]

        if isinstance(e, type):
            if issubclass(e, HelixActor):
                return e.allVisitKeys[0:1]
            else:
                return [e.__name__]

        raise TypeError('Cannot get key for view: %r' % (e,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BasicGLView(HelixView):
    _buildViews_ = BuildVisitTypeViews()
    viewFactory = RenderViewFactoryVisitor()
    viewForKeys = []

    def __init__(self, actor=None):
        pass
    def resize(self, actor, size):
        pass
    def render(self, actor):
        pass

