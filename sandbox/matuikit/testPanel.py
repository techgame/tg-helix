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

from __future__ import with_statement

from TG.openGL.raw.gl import *
from TG.openGL import data

from TG.helix.kits.matui.resources.material import MatuiMaterial
from TG.helix.kits.matui.resources.stageMaterial import StageRenderMaterial, StageResizeMaterial

from TG.helix.kits.matui import MatuiStage, MatuiActor
from TG.helix.kits.matui.view import MatuiScene

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ColorMeshRenderer(MatuiMaterial):
    def bind(self, actor, res, mgr):
        return [self.partial(self.render, res)]
    def render(self, res):
        color = res['color'].render()
        res['mesh'].render()

class Panel(MatuiActor):
    box = data.Rect.property()
    color = data.Color.property('#ffff')
    minSize = None
    maxSize = None

    def loadResources(self, resources):
        with resources as (res, factory):
            res.render = ColorMeshRenderer()
            res.mesh = factory.boxMesh(self.box)
            res.color = factory.immediate(self.color)
        self._mesh = res.mesh

    def onCellLayout(self, cell, cbox):
        self.box.centerIn(cbox)
        self._mesh.update(self.box)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SandboxStage(MatuiStage):
    box = data.Rect.property()

    resources = MatuiStage.resources.copy()
    with resources as (res, factory):
        res.resize = factory.multiMaterial([
                StageResizeMaterial(),
                factory.resizeLayoutMaterial(True),
                ])

        res.render = factory.multiMaterial([
                StageRenderMaterial(),
                factory.orthoProjectionMaterial(),
                factory.blendMaterial(),
                ])

    def onSceneSetup(self, scene):
        node = self.newNode()
        self.node = node

        layout = self.newLayout()
        self.resources['layout'] = layout

        panel = Panel()
        panel.box.setSize((640,360))
        node += panel; layout += panel

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    stage = SandboxStage()

    from TG.helix.bridges.wx.basic import BasicRenderSkinModel
    model = BasicRenderSkinModel()
    model.setupStage(stage, MatuiScene)
    model.skinModel()

