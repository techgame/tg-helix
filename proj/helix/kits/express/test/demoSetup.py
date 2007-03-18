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

        layer = Layer('#00:80:00')
        layer.aspect = 1.6
        renderRoot += layer

        @bgLayer.kvwatch('box.*')
        def layerBox(kvw, key, layer=layer):
            layer.box.setAspectSize(layer.aspect, kvw.value.size, .5)

        l2 = Layer('#ff')
        renderRoot += l2

        @layer.kvwatch('box.*')
        def layerBox(kvw, key, l2=l2):
            l2.box.setSize(kvw.value.size - .1, at=.5)

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

