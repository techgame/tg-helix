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

from .uiBaseViews import UIView, glData

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ List Views
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIListView(UIView):
    viewForKeys = ['UIList']
    pos = None
    scale = None

    def init(self, viewable):
        UIView.init(self, None)
        self.viewable = viewable

        viewable._pub_.add(self.onUpdateViews, 'items')
        viewable.items._pub_.add(self.onUpdateViews)

        self.updateViews()
        self.updateBox()

    def onUpdateViews(self, *args):
        self.enqueue(self.updateViews)
    def updateViews(self):
        self.views = self.viewListFor(self.viewable.items)
        self.updateBox()

    def onUpdateBox(self, *args):
        self.enqueue(self.updateBox)
    def updateBox(self):
        if self.viewable.translate:
            self.pos = self.viewable.box.pos.tolist()

        boxScale = getattr(self.viewable, 'boxScale', None)
        if boxScale is not None:
            box = self.viewable.box
            self.pos = (box.pos + boxScale.pos).tolist()

            size = where(box.size > 1, box.size, 1)
            self.scale = (boxScale.size/size).tolist()
        else: 
            self.scale = None

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

