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

import numpy
from numpy import floor, ceil

from TG.observing import ObservableObjectWithProp
from TG.openGL.data import Rect, Vector

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Cell(ObservableObjectWithProp):
    visible = True
    weight = Vector.property([0,0], '2f')
    minSize = Vector.property([0,0], '2f')
    box = Rect.property()

    def __init__(self, weight=0, min=None):
        self.weight[:] = weight

        if min is not None:
            self.minSize[:] = min

    def adjustAxisSize(self, axisSize, axis, isTrial=False):
        return axisSize

    def layoutIn(self, pos, size):
        box = self.box
        ceil(pos, box.pos)
        floor(size, box.size)
        self.onLayout(self, box)

    def layoutHide(self):
        self.box = None

    def onLayout(self, cell, box):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MaxSizeCell(Cell):
    maxSize = Vector.property([0,0], '2f')

    def __init__(self, weight=0, min=None, max=None):
        Cell.__init__(self, weight, min)
        if max is not None:
            self.maxSize[:] = max

    def adjustAxisSize(self, axisSize, axis, isTrial=False):
        maxSize = self.maxSize
        idx = (maxSize > 0) & (maxSize < axisSize)
        axisSize[idx] = maxSize[idx]
        return axisSize

