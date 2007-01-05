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

from TG.openGL.data import ImageTexture

from .unit import MatuiTextureUnit

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiImageTexture(MatuiTextureUnit):
    def isResourceImage(self): 
        return True

    def loadTexture(self):
        self.texture = ImageTexture(self.image)

    image = None
    openImage = staticmethod(PIL.Image.open)
    def loadImage(self, image):
        if isinstance(image, basestring):
            image = self.openImage(image)
        self.image = image
        return self

    def premultiply(self):
        image = self.image
        bands = image.getbands()
        if bands[-1] != 'A':
            raise TypeError("Image does not have an alpha channel as the last band")

        imageData = image.getdata()

        a = imageData.getband(len(bands)-1)
        
        for idx in xrange(len(bands)-1):
            premult = a.chop_multiply(imageData.getband(idx))
            imageData.putband(premult, idx)
Image = MatuiImage

