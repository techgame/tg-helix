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
    def init(self):
        uiModel.UIStage.init(self)

        vp = self.add(uiModel.UIOrthoViewport())
        panel = self.add(uiModel.UIPanel())

        @vp.box._pub_.add
        def onVPChange(vpbox, key):
            panel.box.setRect(vpbox, 1.5, .5)
            panel.color = '#88f' if vpbox.aspect>panel.box.aspect else '#8f8'

        panel2 = self.add(uiModel.UIPanel())
        panel2.color = '#faa4'

        @panel.box._pub_.add
        def obc(bbox, key):
            panel2.box.setRect(bbox, .5, 1)

        panel3 = self.add(uiModel.UIPanel())
        panel3.color = '#aff4'

        @panel.box._pub_.add
        def obc(bbox, key):
            panel3.box.setRect(bbox, .5, 0)

        panel4 = self.add(uiModel.UIPanel())
        panel4.color = '#44f4'

        @panel.box._pub_.add
        def obc(bbox, key):
            panel4.box.setRect(bbox, 2., 1)

        panel5 = self.add(uiModel.UIPanel())
        panel5.color = '#f444'

        @panel.box._pub_.add
        def obc(bbox, key):
            panel5.box.setRect(bbox, 2., 0)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    stage = SandboxStage()

    from TG.helix.bridges.wx.basic import BasicRenderSkinModel
    model = BasicRenderSkinModel()
    model.setupStage(stage, uiView.uiViewFactory)
    model.skinModel()

