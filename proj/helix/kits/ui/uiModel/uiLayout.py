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
from numpy import vstack, zeros_like, floor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Cell(object):
    visible = True

    def __init__(self, weight=0, minSize=(0,0,0), maxSize=(0,0,0)):
        self.weight = weight
        self.minSize = numpy.array(minSize)
        self.maxSize = numpy.array(maxSize)

    def layoutIn(self, pos, size):
        self.box = Rect.fromPosSize(pos, size)
        print self.weight, self.box
        return self.box.size

class LayoutBase(object):
    def layout(self, cells, box):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

class AxisLayout(object):
    axis = numpy.array([1,0,0], 'b')
    def layout(self, cells, box):
        # determin hidden
        visCells = self.cellsVisible(cells)

        # determin minsize
        weights, minSizes, maxSizes = self.cellsStats(visCells)

        axis = self.axis
        nonAxisSize = (1-axis)*box.size

        minSizes *= axis
        maxSizes *= axis
        availSize = (axis*box.size) - minSizes.sum(0)

        weightSum = weights.sum()
        axisSize = (minSizes + weights*availSize/weightSum)

        # now we deal with max sizes that have been exceeded, redistributing
        # them to other items
        idxMaxSizes = (weights > 0).any(-1) & (maxSizes > 0).any(-1)
        while True:
            idxOverage = idxMaxSizes & (axisSize > maxSizes).any(-1)
            if not idxOverage.any():
                break

            deltaWeights = weights[idxOverage].sum()
            weights[idxOverage] = 0

            deltaSize = axisSize[idxOverage] - maxSizes[idxOverage]
            axisSize[idxOverage] -= deltaSize

            weightSum -= deltaWeights
            if weightSum <= 0:
                # we can't fill up the layout because we've run out of cells to grow
                break

            availSize = deltaSize.sum(0)
            axisSize += weights*availSize/weightSum

        # trim the axisSize to whole integers
        axisSize = floor(axisSize)

        pos = box.pos.copy()
        # let each cell know it's new pos and size
        for idx, c in enumerate(visCells):
            c.layoutIn(pos, axisSize[idx] + nonAxisSize)
            pos += axisSize[idx]

    def cellsVisible(self, cells):
        isItemVisible = self.isItemVisible
        return [i for i in cells if isItemVisible(i)]
    def isItemVisible(self, item):
        return item.visible

    def cellsStats(self, cells):
        minSizes = []
        maxSizes = []
        weights = []
        for i in cells:
            weights.append(i.weight)
            minSizes.append(i.minSize)
            maxSizes.append(i.maxSize)
        return (vstack(weights), vstack(minSizes), vstack(maxSizes))

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
        Cell(1, (100, 100, 0), (200,200,0)),
        Cell(0, (100, 100, 0)),
        ]

    vl = VLayout()
    vl.layout(cells, Rect.fromPosSize((200,200), (800, 800)))

