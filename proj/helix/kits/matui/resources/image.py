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

from TG.openGL.data.image import ImageTextureRect as ImageTexture

from .units import MatuiLoaderMixin, MatuiTextureUnit

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Loader mixin
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ImageLoaderMixin(MatuiLoaderMixin):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiImageTexture(MatuiTextureUnit):
    def isResourceImage(self): 
        return True

    image = None

    def __init__(self, image=None):
        if image is not None:
            self.load(image)

    def bind(self):
        texture = self.texture
        if texture is None and self.image is not None:
            texture = ImageTexture(self.image)
            self.texture = texture
        return texture

    openImage = staticmethod(PIL.Image.open)
    def load(self, image, size=None):
        if isinstance(image, basestring):
            image = self.openImage(image)
        if size is not None:
            image = image.resize(size)
        self.image = image
        return image

    def premultiply(self, raiseOnInvalid=True):
        image = self.image
        if image is None:
            if raiseOnInvalid:
                raise ValueError("Image is None")
            else: return self

        bands = image.getbands()
        if bands[-1] != 'A':
            if raiseOnInvalid:
                raise TypeError("Image does not have an alpha channel as the last band")
            else: return self

        imageData = image.getdata()

        a = imageData.getband(len(bands)-1)
        
        for idx in xrange(len(bands)-1):
            ba = a.chop_multiply(imageData.getband(idx))
            imageData.putband(ba, idx)

        return self
ImageLoaderMixin._addLoader_(MatuiImageTexture, 'imageTexture')

