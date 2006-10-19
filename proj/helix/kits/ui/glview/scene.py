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
from TG.helix.framework.scene import HelixScene

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
        self.viewable = viewable
    def resize(self, size):
        pass
    def render(self):
        pass

    def renderSubviews(self, subviews=None):
        if subviews is None: 
            subviews = self.subviews
        for v in subviews:
            v.render()

uiViewFactory = UIView.registerViewFactory(UIView)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIScene(HelixScene):
    viewForKeys = 'UIStage'

    def __init__(self, stage=None):
        self.init(stage)

    @classmethod
    def fromViewable(klass, stage):
        return klass(stage)

    def init(self, stage):
        super(UIScene, self).init()
        if not stage.isHelixStage():
            raise ArgumentError("Expected an object supporting helix stage protocol")

        self.stage = stage
        for item in stage.items:
            self.subviews.add(self.viewFactory(item))

    def resize(self, ctx, size):
        for view in self.subviews:
            view.resize(size)
        return True

    def refresh(self, ctx):
        for view in self.subviews:
            view.render()
        return True
UIScene.registerViewFactory(UIScene, uiViewFactory)

