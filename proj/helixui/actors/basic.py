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

from TG.helixui.geometry import geometry
from TG.helixui.actors.helix import HelixActor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Bounds(HelixActor):
    visitKind = "Bounds"

    box = None

    @property
    def v(self):
        return self.box.v
    def size(self):
        return self.box.size

    def setCell(self, aCell):
        self.setBox(aCell.box)
    def setBox(self, aBox):
        self.box = aBox.copy()
    def setDims(self, w=2, h=2, d=2):
        self.box = geometry.axisBoxFromDims(w, h, d)
    def setSize(self, w, h, d=1):
        self.box = geometry.axisBoxFromSize(w, h, d)
    def setPos(self, v, size):
        self.box = geometry.axisBoxFromPos(v, size)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewportBounds(Bounds):
    visitKind = "ViewportBounds"

    def xywh(self):
        return map(int, self.v[0:2, 0:2].flat)
    def setViewportSize(self, size):
        self.setSize(size[0], size[1])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Cell(HelixActor):
    """A basic object rooted in a space"""

    visitKind = "Cell"

    bounds = None
    BoundsFactory = Bounds

    def init(self):
        super(Cell, self).init()
        self.bounds = self.BoundsFactory()
        self.bounds.setDims()

    @property
    def box(self):
        return self.bounds.box

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Widget(Cell):
    """A Widget is a cell that actually displays something.
    
    Widgets may be composite objects, providing spaces to be occupied.
    """

    visitKind = "Widget"

