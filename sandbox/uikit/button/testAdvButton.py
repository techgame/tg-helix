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
        button = self.add(uiModel.UIPanel())

        @vp.box._pub_.add
        def onVPChange(vpbox, key, info=None, button=button):
            button.box.setRect(vpbox, 1.5, .5)
            button.color = '#88f' if vpbox.aspect>button.box.aspect else '#8f8'

        button2 = self.add(uiModel.UIPanel())
        button2.color = '#faa4'

        @button.box._pub_.add
        def obc(bbox, key, info=None, bt2=button2):
            bt2.box.setRect(bbox, .5, 1)

        button3 = self.add(uiModel.UIPanel())
        button3.color = '#aff4'

        @button.box._pub_.add
        def obc(bbox, key, info=None, bt3=button3):
            bt3.box.setRect(bbox, .5, 0)

        button4 = self.add(uiModel.UIPanel())
        button4.color = '#44f4'

        @button.box._pub_.add
        def obc(bbox, key, info=None, bt4=button4):
            bt4.box.setRect(bbox, 2., 1)

        button5 = self.add(uiModel.UIPanel())
        button5.color = '#f444'

        @button.box._pub_.add
        def obc(bbox, key, info=None, bt5=button5):
            bt5.box.setRect(bbox, 2., 0)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    stage = SandboxStage()

    from TG.helix.bridges.wx.basic import BasicRenderSkinModel
    model = BasicRenderSkinModel()
    model.setupStage(stage, uiView.uiViewFactory)
    model.skinModel()

