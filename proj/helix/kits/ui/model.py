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

from TG.openGL.data.rect import Rect
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
        super(Panel, self).init()
        self.items = self.ItemsFactory()

