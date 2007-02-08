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

from TG.helix.events.timerEvents import TimerEventHandler
from TG.helix.kits.matui.resources.material import MatuiMaterial
from TG.helix.kits.matui.resources.stageMaterial import StageRenderMaterial, StageResizeMaterial

from TG.helix.kits.matui import MatuiStage, MatuiActor
from TG.helix.kits.matui.view import MatuiScene

import aglUtils
import qtMacUtils

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MovieHostRenderer(MatuiMaterial):
    def bind(self, actor, res, mgr):
        return [self.partial(self.render, actor)]
    def render(self, actor):
        actor.movieHost.process()

class MovieHost(MatuiActor):
    def __init__(self):
        MatuiActor.__init__(self)
        self.movieHost = qtMacUtils.QTMoiveHost()
        self.movieHost.process()

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
        texMovie.renderDirect()

        #if actor.movie.isDone():
        #    print 'movie is done'

class Movie(MatuiActor):
    def __init__(self, movieHost, moviePath):
        MatuiActor.__init__(self)
        self.movie = qtMacUtils.QTMovie(movieHost)

        if '://' in moviePath:
            self.movie.loadURL(moviePath)
        else: self.movie.loadPath(moviePath)

        self.movie.start()
        self.texMovie = self.movie.texMovie

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

        #self.movie = Movie(self.movieHost.movieHost, 'http://techgame.net/~shane/iSight.mov')
        #self.movie = Movie(self.movieHost.movieHost, 'http://techgame.net/~shane/cercle.mov')
        self.movie = Movie(self.movieHost.movieHost, 'http://213.229.27.207/cgi-bin/video320x240.mjpg?dummy=garb')
        #self.movie = Movie(self.movieHost.movieHost, 'cercle.mov')
        #self.movie = Movie(self.movieHost.movieHost, 'iSight.mov')
        node += self.movie

    timerFrequency = 60
    def onSceneAnimate(self, scene, hostView, info):
        self.movie.movie.processAll(10)
        self.movieHost.movieHost.process()
        scene.performRender(hostView)

    def onSceneSetup(self, scene):
        MatuiStage.onSceneSetup(self, scene)
        scene.evtRoot += TimingEventHandler(scene)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TimingEventHandler(TimerEventHandler):
    def __init__(self, scene):
        self.scene = scene

    def timer(self, hostView, info):
        self.scene.stage.onSceneAnimate(self.scene, hostView, info)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    stage = SandboxStage()

    from TG.helix.bridges.wx.basic import BasicRenderSkinModel
    model = BasicRenderSkinModel()
    model.setupStage(stage, MatuiScene)
    model.skinModel()

