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

from helix import Cell

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SpaceBox(HelixActor):
    """Transform and volume (bounding box).  
    
    Location, orientation, and volume.
    """
    
    pts = None
    size = None

    def updateFromSize(self, (x1, y1)):
        self.update((0., 0.), (x1, y1))

    def update(self, (x0, y0), (x1, y1)):
        if x0 > x1: x0, x1 = x1, x0
        if y0 > y1: y0, y1 = y1, y0

        pts = self.geom.vec([[x0, y0], [x1, y1]])
        size = pts[1]-pts[0]

        self.pts = pts
        self.size = size
        self.aspect = size[0]/size[1]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Cell(HelixActor):
    """A basic object rooted in a space"""

    space = None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LayoutCell(Cell):
    """LayoutCell divides space it occupies into subspaces for cells under it.  
    
    Follows the composite pattern.
    """

    strategy = None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LayerCell(LayoutCell):
    """LayerCell is a LayoutCell that generally divides subspaces by depth"""


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Layout Strategies
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LayoutStrategy(object):
    pass

class LayoutAlign(LayoutStrategy):
    pass

class LayoutGrow(LayoutStrategy):
    pass

class LayoutVertical(LayoutStrategy):
    pass

