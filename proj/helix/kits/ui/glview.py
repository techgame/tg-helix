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

from TG.openGL.data import Vector
from TG.openGL.raw.gl import *
from TG.openGL.raw.glext import GL_TEXTURE_RECTANGLE_ARB

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
        size = Vector(list(size)+[0])

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

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

class UIView(HelixView):
    viewForKeys = []
    viewFactory = uiViewFactory

    def __init__(self, viewable=None):
        self.init(viewable)

    @classmethod
    def fromViewable(klass, viewable):
        return klass(viewable)

    def init(self, viewable):
        pass
    def resize(self, size):
        pass
    def render(self):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewportView(UIView):
    viewForKeys = ['Viewport'] 

    def init(self, viewport):
        self.viewport = viewport

    def resize(self, size):
        self.viewport.onViewResize(size)

        box = self.viewport.box
        x, y = box.pos[:2]
        w, h = box.size[:2]

        glViewport(x, y, w, h)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def render(self):
        glLoadIdentity()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OrthoViewportView(ViewportView):
    viewForKeys = ['OrthoViewport'] 

    def resize(self, size):
        self.viewport.box.size = size

        box = self.viewport.box
        x, y, z = box.pos[:3]
        w, h, d = box.size[:3]
        if z == d == 0:
            z = -10
            d =  20

        glViewport(x, y, w, h)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(x, x+w, y, y+h, z, z+d)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Widget Views
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class WidgetView(UIView):
    viewForKeys = ['Widget']

    def init(self, widget):
        self.widget = widget
        widget.widgetView = self

    def render(self):
        self.renderBox(self.widget)

    def renderBox(self, widget):
        if widget.color is not None:
            glColor4f(*widget.color.flat[:4])

        r = widget.box

        v00 = r.v0[:3]
        v10 = v00.copy()
        v11 = r.v1[:3]
        v01 = v00.copy()

        v10[0] = v11[0]
        v01[1] = v11[1]

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_TEXTURE_RECTANGLE_ARB)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)

        #glColor3ub(0xff, 0, 0)
        #glBegin(GL_LINE_LOOP)
        glBegin(GL_QUADS)
        glVertex3f(*v00)
        glVertex3f(*v01)
        glVertex3f(*v11)
        glVertex3f(*v10)
        glEnd()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ImageView(WidgetView):
    viewForKeys = ['Image']

    def render(self):
        self.renderBox(self.widget)

class PanelView(WidgetView):
    viewForKeys = ['Panel']

    def init(self, panel):
        WidgetView.init(self, panel)
        self.children = self.viewListFor([])

    def render(self):
        panel = self.widget
        self.renderBox(panel)

        for e in self.children:
            e.render()

class ButtonView(WidgetView):
    viewForKeys = ['Button']

    def render(self):
        button = self.widget
        self.renderBox(button)

