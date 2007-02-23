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

import string

from TG.openGL.text import FontRect, Font2d

from .units import MatuiLoaderMixin, MatuiFontUnit

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Loader mixin
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FontLoaderMixin(MatuiLoaderMixin):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Font
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FreetypeFont(MatuiFontUnit):
    FontFactory = Font2d
    #FontFactory = FontRect
    font = None
    def __init__(self, face, size, charset=string.printable, **kw):
        self.loader = self.FontFactory.loaderFromFilename(face, size, charset=charset, **kw)

    def bind(self):
        if self.font is None:
            self.font = self.loader.font
            self.texture = self.font.texture
            self.texture.deselect()
        return self.font
FontLoaderMixin._addLoader_(FreetypeFont, 'freetypeFont')

class FreetypeFontRect(FreetypeFont):
    FontFactory = FontRect
FontLoaderMixin._addLoader_(FreetypeFontRect, 'freetypeFontRect')
class FreetypeFont2d(FreetypeFont):
    FontFactory = Font2d
FontLoaderMixin._addLoader_(FreetypeFont2d, 'freetypeFont2d')

