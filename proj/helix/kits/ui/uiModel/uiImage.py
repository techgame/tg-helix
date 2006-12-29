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

import PIL.Image

from .uiBase import UIItem, UIItemWithBox, glData, numpy
from .uiWidgets import UIWidget

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Images
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UITexture(UIItem):
    viewVisitKeys = ["UITexture"]

    def __init__(self, image=None, **kwattr):
        super(UITexture, self).__init__()

        if image is not None:
            self.loadImage(image)

        if kwattr:
            self.set(kwattr)

    openImage = staticmethod(PIL.Image.open)
    def loadImage(self, image, forceSize=None):
        if isinstance(image, basestring):
            image = self.openImage(image)
        self.image = image

    _image = None
    def getImage(self):
        return self._image
    def setImage(self, image):
        self._image = image
        self.box.size.set(image.size)
    image = property(getImage, setImage)

    def resizeImage(self, size):
        self.image = self.image.resize(size)

    def premultiply(self):
        bands = image.getbands()
        if bands[-1] != 'A':
            raise TypeError("Image does not have an alpha channel as the last band")

        imageData = self.image.getdata()

        a = imageData.getband(len(bands)-1)
        
        for idx in xrange(len(bands)-1):
            premult = a.chop_multiply(imageData.getband(idx))
            imageData.putband(premult, idx)

        return self

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIImage(UIWidget):
    viewVisitKeys = ["UIImage"]

    def __init__(self, image=None, **kwattr):
        super(UIImage, self).__init__()

        if image is not None:
            self.loadImage(image)

        if kwattr:
            self.set(kwattr)

    openImage = staticmethod(PIL.Image.open)
    def loadImage(self, image, forceSize=None):
        if isinstance(image, basestring):
            image = self.openImage(image)
        self.image = image

    _image = None
    def getImage(self):
        return self._image
    def setImage(self, image):
        self._image = image
        self.box.size.set(image.size)
    image = property(getImage, setImage)

    def resizeImage(self, size):
        self.image = self.image.resize(size)

    def premultiply(self):
        image = self.image
        bands = image.getbands()
        if bands[-1] != 'A':
            raise TypeError("Image does not have an alpha channel as the last band")

        imageData = self.image.getdata()

        a = imageData.getband(len(bands)-1)
        
        for idx in xrange(len(bands)-1):
            premult = a.chop_multiply(imageData.getband(idx))
            imageData.putband(premult, idx)

        return self

