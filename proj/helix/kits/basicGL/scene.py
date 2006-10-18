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

from TG.observing import ObservableList
from TG.helix.framework.scene import HelixScene

from TG.helix.kits.general.views import BasicView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewCollection(ObservableList):
    def __init__(self, viewFactory):
        self.viewFactory = viewFactory

    def createViewFor(self, item):
        isHelixView = getattr(item, 'isHelixView', lambda: False)
        if isHelixView():
            return item
        else:
            return item.accept(self.viewFactory)

    def addViewFor(self, item):
        view = self.createViewFor(item)
        if view is not None:
            self.append((item, view))

    def removeViewFor(self, item):
        for i in enumerate(self):
            if views[i][0] is item:
                views.pop(i)
                return True
        else:
            return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BasicGLRenderer(object):
    ViewCollectionFactory = ViewCollection
    def __init__(self, scene, viewFactory):
        scene.views = self.ViewCollectionFactory(viewFactory)

        self.scene = scene
        self._hookScene(scene)

    def _hookScene(self, scene, bAdd=True):
        scene._pub_.hook(bAdd, self.performResize, '@resize')
        scene._pub_.hook(bAdd, self.performRefresh, '@refresh')

    def performResize(self, scene, pubKey, ctx, size):
        for item, view in scene.views:
            view.resize(item, size)
        return True

    def performRefresh(self, scene, pubKey, ctx):
        for item, view in scene.views:
            view.render(item)
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BasicGLScene(HelixScene):
    viewFactory = BasicView.viewFactory
    Renderer = BasicGLRenderer

    def init(self):
        super(BasicGLScene, self).init()
        BasicGLRenderer(self, self.viewFactory)

