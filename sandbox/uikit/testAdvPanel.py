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
        layout = self.layout

        self.add(uiModel.UIOrthoViewport())
        self.add(uiModel.UIBlend())

        panel = self.add(uiModel.UIPanel())

        panel.layout = layout.add('group')

        @layout.evtAdd
        def onlayout(cell, lbox):
            panel.box.setRect(lbox, 1.5, .5)
            panel._kvnotify_("set", "box")
            panel.color = '#88f' if lbox.aspect>panel.box.aspect else '#8f8'
            panel._kvnotify_("set", "color")

            panel.layout.layoutIn(panel.box)

        panel2 = self.add(uiModel.UIPanel())
        panel2.color = '#faa4'

        @panel.layout.evtAdd
        def onlayout(cell, lbox):
            panel2.box.setRect(lbox, .5, 1)
            panel2._kvnotify_("set", "box")

        panel3 = self.add(uiModel.UIPanel())
        panel3.color = '#aff4'

        @panel.layout.evtAdd
        def onlayout(cell, lbox):
            panel3.box.setRect(lbox, .5, 0)
            panel3._kvnotify_("set", "box")

        panel4 = self.add(uiModel.UIPanel())
        panel4.color = '#44f4'

        @panel.layout.evtAdd
        def onlayout(cell, lbox):
            panel4.box.setRect(lbox, 2., 1)
            panel4._kvnotify_("set", "box")

        panel5 = self.add(uiModel.UIPanel())
        panel5.color = '#f444'

        @panel.layout.evtAdd
        def onlayout(cell, lbox):
            panel5.box.setRect(lbox, 2., 0)
            panel5._kvnotify_("set", "box")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    stage = SandboxStage()

    from TG.helix.bridges.wx.basic import BasicRenderSkinModel
    model = BasicRenderSkinModel()
    model.setupStage(stage, uiView.uiViewFactory)
    model.skinModel()

