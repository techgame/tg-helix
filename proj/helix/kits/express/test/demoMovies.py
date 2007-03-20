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
        resizeRoot = scene['resize']

        viewport = Viewport()
        resizeRoot += viewport
        renderRoot += viewport

        projection = Projection()
        resizeRoot += projection
        renderRoot += projection

        bgLayer = BackgroundLayer()
        renderRoot += bgLayer

        @projection.kvwatch('box.*')
        def onProjectionBox(kvw, key, bgbox=bgLayer.box):
            v = kvw.value.pv[..., :-1]
            bgbox.pv = v

        bigMovie = QTMovieLayer(os.path.join(filePath, 'milkgirls1080.mov'), hostBox=bgLayer.box)
        bigMovie.looping()
        renderRoot += bigMovie
        bigMovie.play()

        cameraMovie = QTMovieLayer(os.path.join(filePath, 'cercle.mov'), color='#ff:40', hostBox=bgLayer.box)
        cameraMovie.looping()
        renderRoot += cameraMovie
        cameraMovie.play()

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

