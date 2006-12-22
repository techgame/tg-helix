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

from TG.openGL.raw.gl import *

from TG.helix.kits.ui.uiModel import UIStage, UIItem, UIViewport, UIBlend
from TG.helix.kits.ui.uiView import uiViewFactory, UIView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FunToy(UIItem):
    viewVisitKeys = ['FunToy']
    color = (.2, .8, 1., .5)

class FunToyView(UIView):
    viewForKeys = ['FunToy']

    def init(self, viewable):
        super(FunToyView, self).init(viewable)
        self.viewable = viewable

    def render(self):
        viewable = self.viewable
        glColor4f(*viewable.color)
        glBegin(GL_QUADS)
        glVertex2f(-.9, -.9)
        glVertex2f(.9, -.9)
        glVertex2f(.9, .9)
        glVertex2f(-.9, .9)
        glEnd()

class FunStage(UIStage):
    def load(self):
        self.add(UIViewport())
        self.add(UIBlend())

        self.add(FunToy())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    stage = FunStage()

    from TG.helix.bridges.wx.basic import BasicRenderSkinModel
    model = BasicRenderSkinModel()
    model.setupStage(stage, uiViewFactory)
    model.skinModel()

