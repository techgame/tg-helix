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

from TG.helix.kits.ui import uiModel
from TG.helix.kits.ui import uiView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SandboxStage(uiModel.UIStage):
    def load(self):
        vp = self.add(uiModel.OrthoViewport())
        self.button = self.add(uiModel.Button())
        vp.box._pub_.add(self.onVPChange)

    def onVPChange(self, vpbox, key, info=None):
        box = self.button.box
        box.setRect(vpbox, 1.5)
        box.pos = 0.5 * (vpbox.size - box.size)
        self.button.color.set('#ff0000' if box.pos[0]>box.pos[1] else '#00ff00')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    stage = SandboxStage()
    stage.load()

    from TG.helix.bridges.wx.basic import BasicRenderSkinModel
    model = BasicRenderSkinModel()
    model.setupStage(stage, uiView.uiViewFactory)
    model.skinModel()

