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
from TG.helixui.stage.scene import HelixUIScene, SceneVisitor
from TG.helixui.actors.basic import HelixActor, Widget
from TG.helixui.actors.visitor import HelixMethodVisitor

from TG.openGL.raw import gl, glu, glext
from TG.openGL.raw.gl import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderVisitor(HelixMethodVisitor):
    action = 'render'

    def onVisitScene(self, actor):
        return True

    def onVisitViewportBounds(self, actor):
        glViewport(*actor.xywh())

    def onVisitClearBuffers(self, actor):
        glClearColor(*actor.color)
        glClearDepth(actor.depth)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    def onVisitTestRect(self, actor):
        glColor4f(*actor.color)
        glBegin(GL_QUADS)
        for e in actor.v:
            glVertex3f(*e)
        glEnd()

class ClearBuffers(HelixActor):
    color = (0.01, 0.01, 0.01, 0.0)
    depth = 1.0

class TestRect(Widget):
    color = (1.0, 0.0, 0.0, 0.8)
    v = [[-0.5, -0.5, 0.], [0.5, -0.5, 0.], [0.5, 0.5, 0.], [-0.5, 0.5, 0.]]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestScene(HelixUIScene):
    def loadCommands(self):
        super(TestScene, self).loadCommands()
        self.addCommand(SceneVisitor(RenderVisitor()))

    def loadScene(self):
        super(TestScene, self).loadScene()
        self.items.extend([
                ClearBuffers(),
                TestRect(),
                ])


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestRenderSkinModel(BasicRenderSkinModel):
    SceneFactory = TestScene

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    model = TestRenderSkinModel()
    model.skinModel()

