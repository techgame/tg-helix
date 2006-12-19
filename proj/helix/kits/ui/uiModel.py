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

from TG.observing import Observable, ObservableProperty

from TG.openGL import data as glData
from TG.openGL import text as glText

from TG.helix.framework.stage import HelixStage, HelixActor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ UI Basics
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIStage(HelixStage):
    viewVisitKeys = ["UIStage"]

    def load(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

class UIItem(HelixActor):
    viewVisitKeys = []

    def __init__(self, **kwattr):
        super(UIItem, self).__init__()
        if kwattr:
            self.set(kwattr)

    def set(self, val=None, **kwattr):
        for n,v in (val or kwattr).iteritems():
            setattr(self, n, v)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Viewport settings
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIViewport(UIItem):
    viewVisitKeys = ["UIViewport"]

    box = glData.Recti.property()

    def onViewResize(self, viewSize):
        self.box.size.set(viewSize)

class UIOrthoViewport(UIViewport):
    viewVisitKeys = ["UIOrthoViewport"]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Widgets
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIWidget(UIItem):
    """A Widget is a cell that actually displays something.
    
    Widgets may be composite objects, providing spaces to be occupied.
    """
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

class UIImage(UIWidget):
    viewVisitKeys = ["UIImage"]

    image = None

    def __init__(self, image, **kwattr):
        super(UIImage, self).__init__()
        self.loadImage(image)
        if kwattr:
            self.set(kwattr)

    def loadImage(self, image):
        if isinstance(image, basestring):
            image = self.openImage(image)

        self.image = image
        self.box.size.set(image.size)
    openImage = staticmethod(PIL.Image.open)

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIButton(UIWidget):
    viewVisitKeys = ["UIButton"]

    stateMap = {}
    def addState(self, stateKey, stateImage):
        if not self.stateMap:
            self.stateMap = {}
        stateImg = UIImage(stateImage)

        self.box.growSize(stateImg.box.size)
        stateImg.box = self.box
        self.stateMap[stateKey] = stateImg
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIFont(UIItem):
    viewVisitKeys = ["UIFont"]

    font = None
    def __init__(self, face, size=None, **kw):
        UIItem.__init__(self)
        self.font = glText.fromFace(face, size, **kw)

    @classmethod
    def fromItem(klass, font):
        if isinstance(font, tuple):
            font = klass(*font)
        elif isinstance(font, dict):
            font = klass(**font)
        else:
            font = klass(font)
        return font
        
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
        UIWidget.__init__(self)

        if kwattr:
            self.set(kwattr)

        if text is not None:
            self.text = text

        if font is not None:
            self.font = font

    _font = None
    def getFont(self):
        return self._font
    def setFont(self, font):
        if not isinstance(font, UIItem):
            font = UIFont.fromItem(font)
        self._font = font
    font = property(getFont, setFont)

