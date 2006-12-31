##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#FIXME: Apparently Rects are very time expensive, which is a big speed problem

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from itertools import izip

import numpy
from numpy import empty_like, empty, ndindex

from TG.observing import ObservableObjectWithProp
from TG.openGL.data import Rect, Vector

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Layouts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LayoutBase(ObservableObjectWithProp):
    _nAdjustTries = 3
    outside = Vector.property([0,0], '2f')
    inside = Vector.property([0,0], '2f')

    def layout(self, cells, box, isTrial=False):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def cellsVisible(self, cells):
        return [c for c in cells if c.visible]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Axis Layouts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AxisLayout(LayoutBase):
    axis = Vector.property([0,0], '2b')

    def layout(self, cells, box, isTrial=False):
        if not cells:
            return Rect((box.pos, box.size*0))

        # determin visible cells
        visCells = self.cellsVisible(cells)

        # determin sizes for cells
        axisSizes = self.axisSizesFor(visCells, box, isTrial)

        if not isTrial:
            iCells = iter(visCells)
            iCellBoxes = self.iterCellBoxes(visCells, box, axisSizes, isTrial)

            # let cells lay themselves out in their boxes
            for (cellPos, cellSize), c in izip(iCellBoxes, iCells):
                c.layoutIn(cellPos, cellSize)

            # hide cells that have no box
            for c in iCells:
                c.layoutHide()

        return self.layoutBox(visCells, box, axisSizes, isTrial)

    def axisSizesFor(self, cells, box, isTrial=False):
        # determin minsize
        axis = self.axis
        weights, minSizes = self.cellsStats(cells)

        # calculate the total border size
        borders = axis*(2*self.outside + (len(cells)-1)*self.inside)
        availSize = axis*box.size - borders

        # now remove all the minSize items
        axisSizes = minSizes.copy()
        availSize -= axisSizes.sum(0)

        # if we have any space left over, distribute to weighted items
        if (availSize >= 0).all():
            weightSum = weights.sum()
            if weightSum > 0:
                axisSizes += weights*availSize/weightSum

        # allow the cells to negotiate space and adjust to it
        axisSizes = self.axisSizeAdjust(cells, box, weights, axisSizes, isTrial)
        return axisSizes

    def axisSizeAdjust(self, cells, box, weights, axisSizes, isTrial=False):
        weightSum = weights.sum()

        for x in xrange(self._nAdjustTries):
            # allow cells to adjust for maxsize, rounding, etc
            adjSizes = self.cellsAdjustedSize(cells, axisSizes, isTrial)
            idxAdj = (adjSizes != 0).any(-1)
            if not idxAdj.any():
                # if none changed, we are done
                break

            # adjust as requested
            axisSizes -= adjSizes

            # repartition our adjSize to new weighted ones
            availSize = adjSizes.sum(0)

            # remove those who changed the size from the weights
            weightSum -= weights[idxAdj].sum()
            weights[idxAdj] = 0

            if weightSum > 0:
                # distributed the available size to the remaining weighted items
                axisSizes += weights*availSize/weightSum
            else:
                # if there are no more items to reweight, then we are done
                break

        return axisSizes

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def iterCellBoxes(self, cells, box, axisSizes, isTrial=False):
        axis = self.axis
        outside = self.outside
        nonAxisSize = (1-axis)*(box.size - outside)
        pos = box.pos + outside
        axisBorders = axis*self.inside

        # let each cell know it's new pos and size
        for asize in axisSizes:
            yield pos.copy(), asize + nonAxisSize

            pos += asize + axisBorders
        pos -= axisBorders

    def layoutBox(self, visCells, box, axisSizes, isTrial=False):
        axis = self.axis

        lPos = box.pos
        # non-axis size
        lSize = (1-axis)*box.size
        # plus borders along axis
        lSize += axis*(2*self.outside + (len(axisSizes)-1)*self.inside)
        # plus axis size
        lSize += axisSizes.sum(0)
        return Rect((lPos, lSize))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def cellsStats(self, cells):
        axis = self.axis
        minSizes = empty((len(cells), 2), 'f')
        weights = empty((len(cells), 2), 'f')
        idxWalk = ndindex(weights.shape[:-1])
        for c, idx in izip(cells, idxWalk):
            weights[idx] = axis*(c.weight or 0)
            minSizes[idx] = axis*(c.minSize or 0)
        return (weights, minSizes)

    def cellsAdjustedSize(self, cells, axisSizes, isTrial=False):
        adjSizes = empty_like(axisSizes)
        axis = self.axis
        for c, axSize, adSize in zip(cells, axisSizes, adjSizes):
            adSize[:] = axSize - c.adjustAxisSize(axSize.copy(), axis, isTrial)
        return adjSizes

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HLayout(AxisLayout):
    axis = Vector.property([1,0], '2b')
class VLayout(AxisLayout):
    axis = Vector.property([0,1], '2b')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    from uiLayoutCells import *
    cells = [
        Cell(0, 200),
        MaxSizeCell(1, 200, 300),
        Cell(1, 200),
        ]

    vl = VLayout()
    vl.inside.set(10)
    vl.outside.set((50, 50, 0))

    box = Rect.fromPosSize((0,0), (1000, 1000))
    if 0:
        for p in xrange(2):
            lb = vl.layout(cells, box, not p%2)
            print
            print 'box:', box
            print '  layout:', lb
            for i, c in enumerate(cells):
                print '    cell %s:' % i, c.box
            print

    # timing analysis
    if 1:
        import time

        n = 100
        box.size *= 5
        cells *= 10
        cn = max(1, len(cells)*n)

        if 1:
            s = time.time()
            for p in xrange(n):
                vl.layout(cells, box, False)
            dt = time.time() - s
            print dt, dt/cn, cn/dt

        if 1:
            s = time.time()
            for p in xrange(n):
                vl.layout(cells, box, True)
            dt = time.time() - s
            print dt, dt/cn, cn/dt

