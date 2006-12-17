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

from TG.openGL.data.image import ImageTexture

from .uiViewBase import UIView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Widget Views
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIWidgetView(UIView):
    viewForKeys = ['UIWidget']

    partsByName = ['color', 'box']

    def init(self, widget):
        UIView.init(self, widget)
        self.update(widget)

    def _onViewableChange(self, viewable, attr, info=None):
        UIView._onViewableChange(self, viewable, attr, info=None)

        if attr in self.partsByName:
            self.update(viewable, [attr])

    def update(self, widget, partNames=None):
        if partNames is None:
            partNames = self.partsByName

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

    partsByName = ['color', 'imageTexView', 'texCoordsView', 'box']

    imageTex = ImageTexture.property()

    def init(self, uiImage):
        UIWidgetView.init(self, uiImage)

        self.imageTex.loadImage(uiImage.image)
        self.imageTexView = self.viewFactory(self.imageTex)
        self.texCoords = self.imageTex.texCoordsForImage()
        self.texCoordsView = self.viewFactory(self.texCoords)

