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

from TG.openGL.data import Rect

import numpy
from numpy import vstack, zeros_like, floor, ceil

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Cell(object):
    visible = True

    def __init__(self, weight=0, minSize=(0,0,0), maxSize=(0,0,0)):
        self.weight = weight
        self.minSize = numpy.array(minSize)
        self.maxSize = numpy.array(maxSize)

    def adjustAxisSize(self, axisSize, axis):
        maxSize = self.maxSize
        idx = (maxSize > 0) & (maxSize < axisSize)
        axisSize[idx] = maxSize[idx]
        return axisSize

    def layoutIn(self, pos, size):
        self.box = Rect.fromPosSize(ceil(pos), floor(size))
        print self.weight, self.box
        return self.box.size

class LayoutBase(object):
    def layout(self, cells, box):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

class AxisLayout(object):
    axis = numpy.array([1,0,0], 'b')
    _passToken = 0
    def layout(self, cells, box):
        passToken = self._passToken + 1
        self._passToken = passToken

        # determin hidden
        visCells = self.cellsVisible(cells, passToken)

        # determin minsize
        weights, minSizes = self.cellsStats(visCells, passToken)

        axis = self.axis

        minSizes *= axis
        availSize = (axis*box.size) - minSizes.sum(0)

        weightSum = weights.sum()
        axisSizes = minSizes + weights*availSize/weightSum

        # allow cells to adjust for maxsize, rounding, etc
        for x in xrange(10): # max of ten tries
            adjSizes = self.cellsAdjustedSize(visCells, passToken, axisSizes, axis)
            idxAdj = (adjSizes != 0).any(-1)
            if not idxAdj.any():
                break

            axisSizes -= adjSizes
            availSize = adjSizes.sum(0)

            weightSum -= weights[idxAdj].sum()
            weights[idxAdj] = 0

            if weightSum <= 0:
                break

            axisSizes += weights*availSize/weightSum

        fpos, fsize = self.cellsLayoutIn(visCells, passToken, axisSizes, axis, box)

        return box.fromPosSize(fpos, fsize)

    def cellsVisible(self, cells, passToken):
        isItemVisible = self.isItemVisible
        return [c for c in cells if isItemVisible(c)]
    def isItemVisible(self, item):
        return item.visible

    def cellsStats(self, cells, passToken):
        minSizes = []
        weights = []
        for c in cells:
            weights.append(c.weight)
            minSizes.append(c.minSize)
        return (vstack(weights), vstack(minSizes))

    def cellsAdjustedSize(self, cells, passToken, axisSizes, axis):
        adjSizes = []
        for c, asize in zip(cells, axisSizes):
            adjSizes.append(asize - c.adjustAxisSize(asize.copy(), axis))
        return vstack(adjSizes)

    def cellsLayoutIn(self, cells, passToken, axisSizes, axis, box):
        nonAxisSize = (1-axis)*box.size
        pos = box.pos.copy()

        # let each cell know it's new pos and size
        for idx, c in enumerate(cells):
            c.layoutIn(pos, axisSizes[idx] + nonAxisSize)
            pos += axisSizes[idx]

        return box.pos, (axisSizes.sum(0) + nonAxisSize)


class HLayout(AxisLayout):
    axis = numpy.array([1,0,0], 'b')
class VLayout(AxisLayout):
    axis = numpy.array([0,1,0], 'b')
class DLayout(AxisLayout):
    axis = numpy.array([0,0,1], 'b')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    cells = [
        Cell(0, (100, 100, 0)),
        Cell(1, (100, 100, 0)),# (200,200,0)),
        Cell(.5, (100, 100, 0)),
        ]

    vl = VLayout()
    print vl.layout(cells, Rect.fromPosSize((200,200), (800, 800)))

