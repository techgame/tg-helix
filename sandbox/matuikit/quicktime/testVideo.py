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

import aglUtils
import qtMacUtils

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MovieHostRenderer(MatuiMaterial):
    def bind(self, actor, res, mgr):
        return [self.partial(self.render, actor)]
    def render(self, actor):
        pass
        #actor.movieHost.process()

class MovieHost(MatuiActor):
    def __init__(self):
        MatuiActor.__init__(self)
        self.movieHost = qtMacUtils.QTMoiveHost()
        #self.movieHost.process()

    def loadResources(self, resources):
        with resources as (res, factory):
            res.render = MovieHostRenderer()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MovieRenderer(MatuiMaterial):
    def bind(self, actor, res, mgr):
        return [self.partial(self.render, actor)]
    def render(self, actor):
        texMovie = actor.texMovie
        texMovie.update()

        x,y = actor.box.pos
        gl.glPushMatrix()
        gl.glTranslatef(x,y,0)
        texMovie.renderDirect()
        gl.glPopMatrix()

        actor.movie.process()

class Movie(MatuiActor):
    box = data.Rect.property()

    def __init__(self, movieHost, moviePath, bLooping=True):
        MatuiActor.__init__(self)
        self.movie = qtMacUtils.QTMovie(movieHost)

        if '://' in moviePath:
            self.movie.loadURL(moviePath)
        else: self.movie.loadPath(moviePath)

        if bLooping:
            self.movie.setLooping()

        self.movie.process(100)
        self.texMovie = self.movie.texMovie
        self.texMovie.update(True)
        print self.texMovie.movieSize
        self.box.size[:] = self.texMovie.movieSize

        self.movie.start()

    def loadResources(self, resources):
        with resources as (res, factory):
            res.render = MovieRenderer()

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

    def loadForScene(self, scene):
        node = self.newNode()
        self.node = node

        layout = self.newLayout()
        self.resources['layout'] = layout

        aglUtils.setAGLSwapInterval()
        self.movieHost = MovieHost()
        node += self.movieHost

        self.movieA = Movie(self.movieHost.movieHost, 'cercle.mov', True)
        self.movieA.box.pos = (100,100)
        node += self.movieA

        self.movieB = Movie(self.movieHost.movieHost, 'iSight.mov')
        node += self.movieB
        self.movieB.box.pos = self.movieA.box.posAt((1,0))+(10,0)

        self.movieC = Movie(self.movieHost.movieHost, 'cercle.mov')
        node += self.movieC
        self.movieC.box.pos = self.movieB.box.posAt((1,0))+(10,0)

    timerFrequency = 60
    def onSceneAnimate(self, scene, hostView, info):
        scene.performRender(hostView)

    def onSceneSetup(self, scene):
        MatuiStage.onSceneSetup(self, scene)
        scene.evtRoot += MatuiAnimationEventHandler(scene)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    stage = SandboxStage()

    from TG.helix.bridges.wx.basic import BasicRenderSkinModel
    model = BasicRenderSkinModel()
    model.setupStage(stage, MatuiScene)
    model.skinModel()

