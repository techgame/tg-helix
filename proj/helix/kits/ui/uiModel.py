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

from TG.openGL import data as glData

from TG.helix.framework.stage import HelixStage, HelixActor

from TG.observing import ObservableTypeParticipant

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ UI Basics
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIStage(HelixStage):
    viewVisitKeys = ["UIStage"]

class UIItem(HelixActor):
    viewVisitKeys = []

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Viewport settings
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Viewport(UIItem):
    viewVisitKeys = ["Viewport"]

    def init(self):
        super(Viewport, self).init()
        self.box = glData.Rect(dtype='i')

    def onViewResize(self, viewSize):
        self.box.size = viewSize

class OrthoViewport(Viewport):
    viewVisitKeys = ["OrthoViewport"]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Widgets
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Widget(UIItem):
    """A Widget is a cell that actually displays something.
    
    Widgets may be composite objects, providing spaces to be occupied.
    """
    viewVisitKeys = ["Widget"]

    box = glData.Rect()
    color = None

    def init(self):
        super(Widget, self).init()
        if self.color is not None:
            self.color = glData.Color(self.color)
        if self.box is not None:
            self.box = glData.Rect(self.box)

class Button(Widget):
    viewVisitKeys = ["Button"]

    color = '#fff'

class Geometry(UIItem):
    pass

