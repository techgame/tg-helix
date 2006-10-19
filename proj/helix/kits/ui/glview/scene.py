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

from TG.helix.framework.views import HelixView
from TG.helix.framework.scene import HelixScene, notifier

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIView(HelixView):
    def __init__(self, viewable=None):
        self.init(viewable)

    @classmethod
    def fromViewable(klass, viewable):
        return klass(viewable)

    def init(self, viewable):
        pass
    def resize(self, viewable, size):
        pass
    def render(self, viewable):
        pass
UIView.registerViewFactory(UIView)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GLUIRenderer(object):
    def __init__(self, scene, viewFactory):
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

class UIScene(HelixScene):
    viewFactory = UIView.viewFactory
    RendererFactory = GLUIRenderer

    @notifier
    def init(self):
        super(UIScene, self).init()
        self.RendererFactory(self, self.viewFactory)

