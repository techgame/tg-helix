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

from TG.openGL.raw import gl
from TG.openGL.data.image import ImageTexture

from .uiBaseViews import UIView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Widget Views
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIWidgetView(UIView):
    viewForKeys = ['UIWidget']

    partsByName = ['color', 'box']

    def init(self, widget):
        UIView.init(self, widget)
        self.update(widget, self.partsByName)

    def _onViewableChange(self, viewable, attr):
        UIView._onViewableChange(self, viewable, attr)

        if attr in self.partsByName:
            self.update(viewable, [attr])

    def update(self, widget, partNames=None):
        for name in partNames:
            part = getattr(widget, name, None)
            if part is not None:
                partView = self.viewFactory(part)
                setattr(self, name, partView)

    def render(self):
        UIView.render(self)
        for attr in self.partsByName:
            getattr(self, attr).render()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIImageView(UIWidgetView):
    viewForKeys = ['UIImage']

    partsByName = ['color', 'box']

    imageTex = ImageTexture.property()

    def init(self, uiImage):
        UIWidgetView.init(self, uiImage)

        self.imageTex.loadImage(uiImage.image)
        self.texCoords = self.imageTex.texCoordsForImage()
        self.texCoordsView = self.viewFactory(self.texCoords)

    def render(self):
        UIView.render(self)

        self.select()
        self.color.render()
        self.texCoordsView.render()
        self.box.render()
        self.deselect()

    def select(self):
        self.imageTex.select()

    def deselect(self):
        self.imageTex.deselect()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIButtonView(UIWidgetView):
    viewForKeys = ['UIButton']

    partsByName = ['color', 'stateui']

    def init(self, uiButton):
        UIWidgetView.init(self, uiButton)
        self.uiButton = uiButton
        uiButton._pub_.add(self.updateBox, 'box')
        uiButton.box._pub_.add(self.updateBox)
        self.onUpdateBox()

    def updateBox(self, box, attr=None):
        self.enqueue(self.onUpdateBox)
    def onUpdateBox(self):
        self.pos = self.uiButton.box.pos.tolist()

    pos = (0,0,0)
    def render(self):
        self.performQueueActions()
        gl.glPushMatrix()
        try:
            gl.glTranslatef(*self.pos)
            UIWidgetView.render(self)
        finally:
            gl.glPopMatrix()

