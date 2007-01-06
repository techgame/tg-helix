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

from . import base
from . import events
from . import sceneManagers

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiScene(base.MatuiView):
    viewForKeys = ['MatuiStage']

    def __repr__(self):
        return '%s: %r' % (self.__class__.__name__, self.stage)

    def isHelixScene(self):
        return True
    def accept(self, visitor):
        return visitor.visitScene(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    stage = None
    def init(self, stage):
        self.stage = stage
        self.box = stage.box
        stage.loadForScene(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setup(self, evtSources=[], **kwinfo):
        self.managers = {}
        self.setupManagers(self.managers)

        self.setupEvtSources(evtSources)

        self.stage.onSceneSetup(self)
        return True

    def shutdown(self):
        self.stage.onSceneShutdown(self)
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    evtRoot = events.MatuiEventRoot.property()
    def setupEvtSources(self, evtSources=[]):
        self.evtRoot.configFor(self, evtSources)

    def setupManagers(self, managers):
        managers.update(
            render=sceneManagers.RenderManager(self),
            resize=sceneManagers.ViewportResizeManager(self),
            select=sceneManagers.SelectManager(self),
            layout=sceneManagers.LayoutManager(self),
            )
        self._animate = managers['render'].render

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Perform Actions from scene event handlers
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def performResize(self, glview, viewportSize):
        resizeMgr = self.managers['resize']
        resizeMgr.resize(glview, viewportSize)

        layoutMgr = self.managers['layout']
        return layoutMgr.layout(glview)

    def performRender(self, glview):
        renderMgr = self.managers['render']
        return renderMgr.render(glview)

    def performSelect(self, glview, pos):
        selectMgr = self.managers['select']
        return selectMgr.select(glview, pos)

    def performAnimation(self, glview, info):
        if 1:
            self.performRender(glview)

