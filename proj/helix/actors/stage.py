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

from .base import HelixObject

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixActor(HelixObject):
    """An actor is simply a participant on the Stage"""

    def isActor(self): return True

    def packagedInNode(self, nodeFactory):
        return nodeFactory(self)

Actor = HelixActor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixStage(HelixActor):
    """The stage is the entry point for setup and interaction with the Scene mediator.

    It's primary responsibility is to implement the logic of the application,
    but it also allows the implementation of onSceneMETHOD templates to address
    setup, shutdown, and animation.
    """
    def isStage(self): return True

    def onSceneSetup(self, scene):
        pass

    def onSceneShutdown(self, scene):
        pass

    def onSceneAnimate(self, scene, hostView, info):
        pass

Stage =  HelixStage


