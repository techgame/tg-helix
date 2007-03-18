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

from TG.openGL.raw import gl
from TG.openGL import data

from TG.helix.kits.matui.resources.material import MatuiMaterial
from TG.helix.kits.matui.resources.stageMaterial import StageRenderMaterial, StageResizeMaterial

from TG.helix.kits.matui import MatuiStage, MatuiActor
from TG.helix.kits.matui.view import MatuiScene
from TG.helix.kits.matui.view.events import MatuiAnimationEventHandler

from TG.openGL.raw import aglUtils
from TG.quicktime import quickTimeMovie

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MovieRenderer(MatuiMaterial):
    def bind(self, actor, res, mgr):
        return [self.partial(self.render, actor, res)]
    def render(self, actor, res):
        qtTexture = actor.qtTexture
        qtTexture.update()

        x,y = actor.box.pos
        gl.glPushMatrix()
        gl.glTranslatef(x,y,0)
        color = res['color'].render()
        qtTexture.renderDirect()
        gl.glPopMatrix()

        actor.movie.process()

class Movie(MatuiActor):
    color = data.Color.property('#ff:ff')
    box = data.Rect.property()

    def __init__(self, moviePath, looping=0):
        MatuiActor.__init__(self)
        self.movie = quickTimeMovie.QTMovie(moviePath)

        self.movie.setLooping(looping)

        self.movie.process(.05)
        self.qtTexture = self.movie.qtTexture
        self.qtTexture.update(True)
        self.box.size[:] = self.qtTexture.size

        self.movie.start()

    def loadResources(self, resources):
        with resources as (res, factory):
            res.render = MovieRenderer()
            res.color = factory.immediate(self.color)

    def onCellLayout(self, cell, cbox):
        self.box.centerIn(cbox)

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
        MatuiStage.onSceneSetup(self, scene)
        scene.evtRoot += MatuiAnimationEventHandler(scene)
        node = self.newNode()
        self.node = node

        layout = self.newLayout()
        self.resources['layout'] = layout

        aglUtils.setAGLSwapInterval()
        quickTimeMovie.qtEnterMovies()

        self.movieA = Movie('milkgirls1080.mov', 2)
        node += self.movieA
        layout += self.movieA

        self.movieC = Movie('masseffect_x06walkthru_HD720p.mov')
        self.movieC.color.set('#ff:80')
        node += self.movieC
        layout += self.movieC

        self.movieD = Movie('cercle.mov', 2)
        self.movieD.color.set('#00:ff:00:80')
        node += self.movieD
        layout += self.movieD

    timerFrequency = 60
    def onSceneAnimate(self, scene, hostView, info):
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    stage = SandboxStage()

    from TG.helix.bridges.wx.basic import BasicRenderSkinModel
    model = BasicRenderSkinModel()
    model.fullscreen = True
    model.setupStage(stage, MatuiScene)
    model.skinModel()

