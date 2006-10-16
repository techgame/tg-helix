#!/usr/bin/env python
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

from numpy.random import random
from TG.observing import ObservableObject, ObservableTypeParticipant

from TG.openGL.raw import gl, glu, glext
from TG.openGL.raw.gl import *

from TG.helixui.bridges.wx.basic import BasicRenderSkinModel
from TG.helixui.framework.scene import HelixScene

from renderWidgets import RenderView, Widget, ViewportBounds, ClearBuffers
from renderCommand import RenderSceneCommand

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Actors
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestWidget(Widget):
    color = (1.0, 0.0, 0.0, 0.8)
    v = [[-0.5, -0.5, 0.], [0.5, -0.5, 0.], [0.5, 0.5, 0.], [-0.5, 0.5, 0.]]
    n = 10

    def __init__(self):
        n = self.n
        self.color = random(4)
        self.v = random(n*3*3).reshape((n*3,3)) * 2. - 1.

    def recolor(self):
        self.color = (self.color + (random(4)/100)) % 1.0
    def reshape(self):
        n = self.n
        self.v = random(n*3*3).reshape((n*3,3)) * 2. - 1.

    def randomly(self):
        if random() > 0.1:
            self.recolor()
        else:
            self.reshape()

class TestWidgetView(RenderView):
    viewForKeys = ['TestWidget']

    def render(self, actor):
        glColor4f(*actor.color)
        glBegin(GL_TRIANGLES)
        for e in actor.v:
            glVertex3f(*e)
        glEnd()
        actor.randomly()

class TestSceneSetupWidget(Widget):
    pass
class TestSceneSetupView(RenderView):
    viewForKeys = ['TestSceneSetupWidget']
    def render(self, actor):
        glEnable(GL_DEPTH_TEST)

        glEnable(GL_COLOR_MATERIAL)
        glShadeModel(GL_SMOOTH)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestScene(HelixScene):
    def load(self):
        RenderSceneCommand(self, RenderView.viewHost)

        self.addViewFor(TestSceneSetupWidget())
        self.addViewFor(ViewportBounds())
        self.addViewFor(ClearBuffers())
        for e in xrange(100):
            self.addViewFor(TestWidget())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestRenderSkinModel(BasicRenderSkinModel):
    SceneFactory = TestScene

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    model = TestRenderSkinModel()
    model.skinModel()

