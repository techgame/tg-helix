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

from TG.helixui.bridges.wx.basic import BasicRenderSkinModel

from TG.helixui.kits.ui import UIStage, ViewportBounds, UIItem

from TG.helixui.kits.ui.views.basicGL import UIScene, UIView, ClearBuffers

from TG.openGL.raw import gl, glu, glext
from TG.openGL.raw.gl import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FunToy(UIItem):
    pass

class FunToyView(UIView):
    viewForKeys = FunToy

    def render(self, actor):
        glColor4f(.2, .8, 1., .5)
        glBegin(GL_QUADS)
        glVertex2f(-1., -1.)
        glVertex2f(1., -1.)
        glVertex2f(1., 1.)
        glVertex2f(-1., 1.)
        glEnd()


class FunStage(UIStage):
    def load(self):
        self.add(self)
        self.add(ViewportBounds())
        self.add(ClearBuffers())
        self.add(FunToyView())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FunUISetupView(UIView):
    viewForKeys = [FunStage]
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
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    model = BasicRenderSkinModel()
    model.scene = UIScene()

    stage = FunStage()
    stage.scene = model.scene
    stage.load()

    model.skinModel()

