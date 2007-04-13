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

from TG.kvObserving import KVProperty, kvobserve
from TG.helix.kits.matui.stage import MatuiStage
from TG.helix.kits.matui.viewport import Viewport

from .scene import TheaterScene
from .host import TheaterHost

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TheaterStage(MatuiStage):
    TheaterScene = TheaterScene
    TheaterHost = TheaterHost

    studioManager = KVProperty(None)
    venue = KVProperty(None)

    def __init__(self, studioManager):
        MatuiStage.__init__(self)
        self.studioManager = studioManager
        self.scene = self.TheaterScene(self)
        self.host = self.TheaterHost(self)

    def onSceneSetup(self, scene):
        self.viewport = Viewport()
        self.kvo('venue', type(self).setupVenue)
        self.setupVenue(self.venue)

    def setupVenue(self, venue):
        root = self.scene.rootNode
        root.clear()

        root += self.viewport

        if venue is not None:
            root += venue

