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

from numpy import where

from TG.openGL.raw import gl

from TG.helix.framework.actors import HelixActorList

from .uiBaseViews import UIView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ List Views
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ListView(UIView):
    viewForKeys = [list]

    def init(self, viewable):
        UIView.init(self, None)
        self.viewable = viewable

    def render(self):
        for view in self.viewFactory.viewsFor(self.viewable):
            view.render()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ObservableListView(UIView):
    viewForKeys = ['UIList', UIView.ViewList, HelixActorList]

    def init(self, viewable):
        UIView.init(self, viewable)
        self.update(viewable)

    def _onViewableChange(self, viewable, attr):
        self.update(viewable)

    def update(self, viewable):
        self.views = self.viewListFor(viewable)

    def render(self):
        for view in self.views:
            view.render()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIListView(UIView):
    viewForKeys = ['UIList']
    pos = None
    scale = None

    def init(self, viewable):
        UIView.init(self, None)
        self.viewable = viewable

        viewable._pub_.add(self.updateViews, 'items')
        viewable.items._pub_.add(self.updateViews)

        viewable._pub_.add(self.updateBox, 'box')
        viewable.box._pub_.add(self.updateBox)

        viewable._pub_.add(self.updateScaling, 'scale')
        viewable._pub_.add(self.updateScaling, 'boxComp')
        viewable.boxComp._pub_.add(self.updateScaling)

        self.updateViews()
        self.onUpdateBox()
        self.onUpdateScaling()

    def updateBox(self, *args):
        self.enqueue(self.onUpdateBox)
    def onUpdateBox(self):
        if self.viewable.translate:
            self.pos = self.viewable.box.pos.tolist()
        self.onUpdateScaling()

    def updateScaling(self, *args):
        self.enqueue(self.onUpdateBox)
    def onUpdateScaling(self):
        if not self.viewable.scale:
            pass

        box = self.viewable.box
        boxComp = self.viewable.boxComp
        self.pos = (box.pos + boxComp.pos).tolist()
        if boxComp.size.any():
            size = where(boxComp.size > 1, boxComp.size, 1)
            self.scale = (box.size/size).tolist()
        else:
            self.scale = None

    def updateViews(self, *args):
        self.views = self.viewListFor(self.viewable.items)

    def render(self):
        UIView.render(self)
        gl.glPushMatrix()
        try:
            if self.pos:
                gl.glTranslatef(*self.pos)
            if self.scale:
                gl.glScalef(*self.scale)

            for view in self.views:
                view.render()
        finally:
            gl.glPopMatrix()

