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

from TG.helix.bridges.wx.basic import BasicRenderSkinModel
from TG.helix.kits.ui.model import UIStage, UIItem, Viewport
from TG.helix.kits.ui.glview import uiViewFactory

import testViews

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FunUISetup(UIItem):
    viewVisitKeys = ['FunUISetup']

class FunToy(UIItem):
    viewVisitKeys = ['FunToy']
    color = (.2, .8, 1., .5)

class FunStage(UIStage):
    def load(self):
        self.add(FunUISetup())
        self.add(Viewport())
        self.add(FunToy())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    stage = FunStage()
    stage.load()

    model = BasicRenderSkinModel()
    model.scene = uiViewFactory(stage)
    model.skinModel()

