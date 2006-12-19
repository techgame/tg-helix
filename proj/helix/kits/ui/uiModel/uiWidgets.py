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

from .uiBase import UIItem, glData, numpy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Widgets
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIWidget(UIItem):
    viewVisitKeys = ["UIWidget"]

    box = glData.Rectf.property()
    color = glData.Color.property([])

    def getPos(self): return self.box.pos
    def setPos(self, pos): self.box.pos.set(pos)
    pos = property(getPos, setPos)

    def getSize(self): return self.box.size
    def setSize(self, size): self.box.size.set(size)
    size = property(getSize, setSize)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIPanel(UIWidget):
    viewVisitKeys = ["UIPanel"]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Images
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
        assert bands[-1] == 'A', bands

        imageData = self.image.getdata()

        a = imageData.getband(len(bands)-1)
        
        for idx in xrange(len(bands)-1):
            premult = a.chop_multiply(imageData.getband(idx))
            imageData.putband(premult, idx)

        self.image = image
        return self

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Button
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIButton(UIWidget):
    viewVisitKeys = ["UIButton"]

    stateMap = {}
    def addState(self, stateKey, stateui):
        if not self.stateMap:
            self.stateMap = {}

        if not isinstance(stateui, UIItem):
            stateui = UIImage.fromItem(stateui)

        self.box.growSize(stateui.box.size)
        self.stateMap[stateKey] = stateui
        if self.state is None:
            self.state = stateKey

    stateui = None
    _state = None
    def getState(self):
        return self._state
    def setState(self, state):
        self.stateui = self.stateMap[state]
        self._state = state
    state = property(getState, setState)

