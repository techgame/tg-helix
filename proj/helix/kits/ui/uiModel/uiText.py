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

from TG.openGL.text.freetypeFontLoader import FreetypeFontLoader

from .uiWidgets import UIItem, UIWidget, glData, numpy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIFont(UIItem):
    viewVisitKeys = ["UIFont"]

    def __init__(self, face, size, **kw):
        super(UIItem, self).__init__()
        self.load(face, size, **kw)

    def load(self, face, size, **kw):
        self._fontLoader = FreetypeFontLoader(face, size, **kw)

    def getFont(self):
        return self._fontLoader.font
    font = property(getFont)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIText(UIWidget):
    viewVisitKeys = ["UIText"]

    font = None
    text = ''
    wrapMode = 'basic'


    line = 1
    lineSpacing = 1
    crop = True

    align = glData.Vector.property([0., 0., 0.], dtype='3f')
    wrapAxis = 0
    roundValues = True

    def __init__(self, text=None, font=None, **kwattr):
        super(UIWidget, self).__init__()

        if kwattr:
            self.set(kwattr)

        if text is not None:
            self.text = text

        if font is not None:
            self.font = font

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _font = None
    def getFont(self):
        return self._font
    def setFont(self, font):
        if not isinstance(font, UIItem):
            font = UIFont.fromItem(font)
        self._font = font
    font = property(getFont, setFont)

