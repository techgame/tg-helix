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

from TG.observing import ObservableList

from renderViews import RenderView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewCollection(ObservableList):
    def __init__(self, scene, viewFactory):
        scene.views = self
        self.viewFactory = viewFactory

    def createViewForActor(self, actor):
        return actor.accept(self.viewFactory)

    def addViewFor(self, actor):
        view = self.createViewForActor(actor)
        self.append((actor, view))

    def removeViewFor(self, actor):
        for i in enumerate(self):
            if views[i][0] is actor:
                views.pop(i)
                return True
        else:
            return False

class RenderSceneCommand(object):
    ViewCollectionFactory = ViewCollection
    def __init__(self, scene, viewFactory):
        self.scene = scene
        scene.views = self.ViewCollectionFactory(scene, viewFactory)

        scene._pub_.add(self.performResize, '@resize')
        scene._pub_.add(self.performRefresh, '@refresh')

    def performResize(self, scene, pubKey, ctx, size):
        for actor, view in scene.views:
            view.resize(actor, size)
        return True

    def performRefresh(self, scene, pubKey, ctx):
        for actor, view in scene.views:
            view.render(actor)
        return True

