#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2007  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import with_statement

import os
filePath = os.path.dirname(__file__)

import numpy

from TG.helix.kits.express import scene, stage
from TG.helix.kits.express.actors import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DemoStage(stage.ExpressStage):
    def onSceneSetup(self, scene):
        renderRoot = scene['render']

        bgLayer = BackgroundLayer()
        scene['resize'] += bgLayer
        renderRoot += bgLayer

        bigMovie = QTMovieLayer(os.path.join(filePath, 'milkgirls1080.mov'))
        bigMovie.looping()
        renderRoot += bigMovie
        bigMovie.play()

        @bgLayer.kvwatch('box.*')
        def updateBox(kvw, key='value', bigMovie=bigMovie, bgLayer=bgLayer):
            bigMovie.box.setAspectWithSize(bigMovie.aspect, bgLayer.box.size, at=0.5)

        cameraMovie = QTMovieLayer(os.path.join(filePath, 'iSight.mov'))
        renderRoot += cameraMovie
        cameraMovie.play()
        cameraMovie.color.a = 0x80

        @bgLayer.kvwatch('box.*')
        def updateBox(kvw, key='value', cameraMovie=cameraMovie, bgLayer=bgLayer):
            cameraMovie.box.setAspectWithSize(cameraMovie.aspect, 0.25*bgLayer.box.size, at=(0.5, 0))

    def onSceneAnimate(self, scene, info):
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    stage = DemoStage()

    from TG.helix.bridges.wx.basic import BasicRenderSkinModel
    model = BasicRenderSkinModel()
    model.setupStage(stage, scene.ExpressScene)
    model.skinModel()

if __name__=='__main__':
    main()

