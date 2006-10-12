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

from TG.helixui.stage.scene import HelixSceneCommand
from renderViews import RenderView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderSceneCommand(HelixSceneCommand):
    def __init__(self, scene):
        self.scene = scene
        scene.addCommand('resize', self.performResize)
        scene.addCommand('renderInitial', self.performRenderInitial)
        scene.addCommand('renderRefresh', self.performRenderRefresh)

    def performResize(self, action, scene, size):
        for actor, view in self.iterViewsForScene(action, scene):
            view.resize(actor, size)
        return True

    def performRenderInitial(self, action, scene, **kw):
        for actor, view in self.iterViewsForScene(action, scene):
            view.renderInitial(actor)
        return True

    def performRenderRefresh(self, action, scene, **kw):
        for actor, view in self.iterViewsForScene(action, scene):
            view.render(actor)
        return True

    def iterViewsForScene(self, action, scene):
        getViewForActor = self.getViewForActor

        view = getViewForActor(scene)
        if view is not None:
            yield scene, view

        for actor in scene.items:
            view = getViewForActor(actor)
            if view is not None:
                yield actor, view

    def getViewForActor(self, actor):
        try: return actor.__view
        except AttributeError: pass

        view = self.createViewForActor(actor)
        actor.__view = view
        return view
    
    def createViewForActor(self, actor):
        return actor.accept(self.viewFactoryVisitor)

    viewFactoryVisitor = RenderView.viewHost

