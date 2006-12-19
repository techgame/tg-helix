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
import numpy

from TG.observing import Observable, ObservableProperty

from TG.openGL import data as glData
from TG.openGL import text as glText
from TG.openGL.text.freetypeFontLoader import FreetypeFontLoader

from TG.helix.framework.stage import HelixStage, HelixActor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ UI Basics
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIStage(HelixStage):
    viewVisitKeys = ["UIStage"]

    def loadForScene(self, scene):
        self.load()
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

    @classmethod
    def fromItem(klass, item):
        if isinstance(item, tuple):
            return klass(*item)
        elif isinstance(item, dict):
            return klass(**item)
        else:
            return klass(item)

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

class UIBlend(UIItem):
    viewVisitKeys = ["UIBlend"]
    flyweights = {
        }
    def __new__(klass, mode):
        self = klass.flyweights.get(mode, None)
        if self is None:
            self = UIItem.__new__(klass, mode)
        return self

    def __init__(self, mode):
        self._mode = mode
        self.flyweights[mode] = self

    _mode = None
    def getMode(self):
        return self._mode
    mode = property(getMode)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Widgets
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIList(UIItem):
    viewVisitKeys = ["UIList"]

    items = UIItem.ActorList.property()
    box = glData.Rectf.property()

    def __init__(self, items, **kwattr):
        if kwattr:
            self.set(kwattr)
        self.items[:] = items
        self.items._pub_.add(self._onItemsChange)

        self.calcBox()

    def _onItemsChange(self, items, attr):
        self.calcBox()

    def calcBox(self):
        pos = numpy.vstack(i.box.pos for i in self.items if hasattr(i, 'box')).min(0)
        corner = numpy.vstack(i.box.corner for i in self.items if hasattr(i, 'box')).max(0)
        box = glData.Rectf.fromCorners(pos, corner)
        self.box = box
        return box

class UIComposite(UIItem):
    viewVisitKeys = ["UIComposite"]
    items = UIItem.ActorList.property()

    box = glData.Rectf.property()
    boxComp = glData.Rectf.property()

    def getPos(self): return self.box.pos
    def setPos(self, pos): self.box.pos.set(pos)
    pos = property(getPos, setPos)

    def getSize(self): return self.box.size
    def setSize(self, size): self.box.size.set(size)
    size = property(getSize, setSize)

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

    _font = None
    def getFont(self):
        return self._font
    def setFont(self, font):
        if not isinstance(font, UIItem):
            font = UIFont.fromItem(font)
        self._font = font
    font = property(getFont, setFont)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIGrid(UIComposite):
    border = glData.Vector.property([10, 10, 0], dtype='3f')
    def __init__(self, gridItems, gridCells, **kwattr):
        super(UIGrid, self).__init__()
        self.gridItems = gridItems
        self.gridCells = gridCells

        if kwattr:
            self.set(kwattr)

        self._pub_.add(self._onGridUpdate)
        self.box._pub_.add(self._onGridUpdate, 'size')
        self.boxComp.size = self.box.size

    def _onGridUpdate(self, item, attr):
        self.layout()

    def layout(self):
        border = self.border
        gridCells = self.gridCells

        fullCellSize = (self.boxComp.size[:2] - border[:2])/self.gridCells
        cellRect = glData.Rect.fromPosSize(border, fullCellSize - border[:2])

        fullCellRect = glData.Rect.fromSize(fullCellSize)
        advRight = fullCellRect.at((1,0,0))
        advDown = -fullCellRect.at((0,1,0))

        gridTopLeft = self.boxComp.at((0, 1, 0)) + (border * (1, -1, 0)) + advDown

        gridItems = []
        iterItems = iter(self.gridItems)
        try:
            for row in xrange(gridCells[1]):
                for col in xrange(gridCells[0]):
                    item = iterItems.next()
                    cellRect.pos.set(gridTopLeft + row*advDown + col*advRight)
                    item.box.setRect(cellRect, item.box.aspect, 0.5)
                    gridItems.append(item)
        except StopIteration:
            pass

        self.items[:] = gridItems

