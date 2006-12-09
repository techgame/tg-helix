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

from functools import partial
from TG.openGL.raw.gl import *

from TG.helix.framework.viewFactory import HelixViewFactory
from TG.helix.framework.views import HelixView
from TG.helix.framework.scene import HelixScene

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

uiViewFactory = HelixViewFactory()

class UIScene(HelixScene):
    viewForKeys = ['UIStage']
    viewFactory = uiViewFactory

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
        self.views = self.viewListFor(stage.items)

    def resize(self, size):
        for view in self.views:
            view.resize(size)
        return True

    def refresh(self):
        self.render()
        for view in self.views:
            view.render()
        return True

    glClearBuffers = staticmethod(partial(glClear, GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT))
    def render(self):
        self.glClearBuffers()

class UIView(HelixView):
    viewForKeys = []
    viewFactory = uiViewFactory

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewportView(UIView):
    viewForKeys = ['Viewport'] 

    def resize(self, size):
        self.viewable.box.size = size
    def render(self):
        box = self.viewable.box
        x, y = box.pos[:2]
        w, h = box.size[:2]
        glViewport(x, y, w, h)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Widget Views
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class WidgetView(UIView):
    viewForKeys = ['Widget']

    def render(self):
        self.renderBounds(widget.bounds, widget.color)

    def renderBounds(self, bounds, color=None):
        rect = bounds.box.vRect()
        if color is not None:
            glColor4f(*color)

        glBegin(GL_QUADS)
        for p in rect:
            glVertex3f(*p)
        glEnd()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ImageView(WidgetView):
    viewForKeys = ['Image']

    def render(self):
        self.viewable = viewable
        self.renderBounds(viewable.bounds, viewable.color)

class PanelView(WidgetView):
    viewForKeys = ['Panel']

    def init(self, panel):
        super(PanelView, self).init(panel)
        self.subviews = self.viewListFor([])

    def render(self):
        panel = self.viewable
        self.renderBounds(panel.bounds, panel.color)
        self.renderSubviews()

class ButtonView(WidgetView):
    viewForKeys = ['Button']

    def render(self):
        viewable = self.viewable
        self.renderBounds(viewable.bounds, viewable.color)

