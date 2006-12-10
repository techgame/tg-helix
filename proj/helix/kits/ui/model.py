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

from TG.openGL.data import Rect, Color, Vector

from TG.helix.framework.stage import HelixStage, HelixActor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIStage(HelixStage):
    viewVisitKeys = ["UIStage"]

class UIItem(HelixActor):
    viewVisitKeys = []

class Viewport(UIItem):
    viewVisitKeys = ["Viewport"]

    box = Rect(dtype='i')
    def init(self):
        self.box = self.box.copy()

    def onViewResize(self, viewSize):
        self.box.size = viewSize

class OrthoViewport(UIItem):
    viewVisitKeys = ["OrthoViewport"]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Widgets
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Widget(UIItem):
    """A Widget is a cell that actually displays something.
    
    Widgets may be composite objects, providing spaces to be occupied.
    """
    viewVisitKeys = ["Widget"]

    box = Rect()

    def init(self):
        self.box = self.box.copy()
        if self._color is not None:
            self._color = self._color.copy()

    _color = None #Color()
    def getColor(self): 
        return self._color
    def setColor(self, color): 
        if color is None:
            self._color = None
            return

        if self._color is None:
            self._color = Color(1)
        self._color.set(color)
    def delColor(self): 
        self._color = None
    color = property(getColor, setColor, delColor)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Button(Widget):
    viewVisitKeys = ["Button"]

class Image(Widget):
    viewVisitKeys = ["Image"]

    def __init__(self, img=None):
        Widget.__init__(self)
        if img is not None:
            self.loadImage(img)

    def loadImage(self, image):
        if isinstance(image, basestring):
            image = self.openImage(filename)
        self.image = image
    openImage = staticmethod(PIL.Image.open)

class Panel(Widget):
    viewVisitKeys = ["Panel"]

    def init(self):
        Widget.init(self)
        self.children = self.ActorList()

