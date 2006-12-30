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
    weight = Vector.property((0,0,0), dtype='3b')
    minSize = Vector.property((0,0,0), dtype='3f')

    def __init__(self, weight=0, min=None):
        self.box = Rect()
        self.weight.set(weight)

        if min is not None:
            self.minSize.set(min)

    def adjustAxisSize(self, axisSize, axis, passToken=0, isTrial=False):
        return axisSize

    def layoutIn(self, pos, size, passToken=0):
        self.box = Rect.fromPosSize(ceil(pos), floor(size))

    def layoutHide(self):
        self.box = None

class MaxSizeCell(Cell):
    maxSize = Vector.property((0,0,0), dtype='3f')

    def __init__(self, weight=0, min=None, max=None):
        Cell.__init__(self, weight, min)
        if max is not None:
            self.maxSize.set(max)

    def adjustAxisSize(self, axisSize, axis, passToken=0, isTrial=False):
        maxSize = self.maxSize
        idx = (maxSize > 0) & (maxSize < axisSize)
        axisSize[idx] = maxSize[idx]
        return axisSize

