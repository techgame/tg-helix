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
from TG.openGL.data.image import ImageTexture

from TG.helix.framework.actors import HelixActorList
from .uiViewBase import UIView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Widget Views
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UICompositeView(UIView):
    viewForKeys = ['UIComposite']

    def init(self, uiComposite):
        UIView.init(self, None)
        self.uiComposite = uiComposite
        uiComposite._pub_.add(self.updateBox, 'box')
        uiComposite._pub_.add(self.updateBox, 'boxComp')
        uiComposite.box._pub_.add(self.updateBox)
        uiComposite.boxComp._pub_.add(self.updateBox)

        uiComposite.items._pub_.add(self.onUpdateItems, 'self')
        self.updateItems(uiComposite.items)
        self.onUpdateBox()

    def updateItems(self, items, attr=None):
        self.enqueue(self.onUpdateItems)
    def onUpdateItems(self):
        self.views = self.viewListFor(self.uiComposite.items)

    def updateBox(self, box, attr=None):
        self.enqueue(self.onUpdateBox)
    def onUpdateBox(self):
        box = self.uiComposite.box
        boxComp = self.uiComposite.boxComp
        self.pos = (box.pos + boxComp.pos).tolist()
        if boxComp.size.any():
            size = where(boxComp.size > 1, boxComp.size, 1)
            self.scale = (box.size/size).tolist()
        else:
            self.scale = (1,1,1)

    pos = (0,0,0)
    scale = (1,1,1)

    def render(self):
        UIView.render(self)
        gl.glPushMatrix()
        try:
            gl.glTranslatef(*self.pos)
            gl.glScalef(*self.scale)
            for view in self.views:
                view.render()
        finally:
            gl.glPopMatrix()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIWidgetView(UIView):
    viewForKeys = ['UIWidget']

    partsByName = ['color', 'box']

    def init(self, widget):
        UIView.init(self, widget)
        self.update(widget, self.partsByName)

    def _onViewableChange(self, viewable, attr, info=None):
        UIView._onViewableChange(self, viewable, attr, info=None)

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

        self.color.render()
        self.imageTex.select()
        self.texCoordsView.render()
        self.box.render()
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ List Views
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ListView(UIView):
    viewForKeys = [list]

    def init(self, uiList):
        UIView.init(self, None)
        self.uiList = uiList

    def render(self):
        for view in self.viewFactory.viewsFor(self.uiList):
            view.render()

class ObservableListView(UIView):
    viewForKeys = ['UIList', UIView.ViewList, HelixActorList]

    def init(self, uiList):
        UIView.init(self, uiList)
        self.update(uiList)

    def _onViewableChange(self, uiList, attr):
        self.update(uiList)

    def update(self, uiList):
        self.views = self.viewListFor(uiList)

    def render(self):
        for view in self.views:
            view.render()

class UIListView(UIView):
    viewForKeys = ['UIList']

    def init(self, uiList):
        UIView.init(self, None)
        self.uiList = uiList
        uiList.items._pub_.add(self.update)
        self.update(uiList.items)
        uiList._pub_.add(self.updateBox, 'box')
        uiList.box._pub_.add(self.updateBox)
        self.onUpdateBox()

    def updateBox(self, box, attr=None):
        self.enqueue(self.onUpdateBox)
    def onUpdateBox(self):
        self.pos = self.uiList.box.pos.tolist()

    def update(self, items, attr=None):
        self.views = self.viewListFor(items)

    pos = (0,0,0)
    def render(self):
        UIView.render(self)
        gl.glPushMatrix()
        try:
            gl.glTranslatef(*self.pos)
            for view in self.views:
                view.render()
        finally:
            gl.glPopMatrix()
