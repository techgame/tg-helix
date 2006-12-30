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

import numpy
from numpy import vstack, zeros_like

from TG.observing import ObservableObjectWithProp
from TG.openGL.data import Rect, Vector

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Layouts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LayoutBase(ObservableObjectWithProp):
    _nAdjustTries = 3
    outside = Vector.property([0,0,0], dtype='3b')
    inside = Vector.property([0,0,0], dtype='3b')

    def layout(self, cells, box, isTrial=False):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _passToken = 0
    def nextPassToken(self):
        passToken = self._passToken + 1
        self._passToken = passToken
        return (self, passToken)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def cellsVisible(self, cells):
        return [c for c in cells if c.visible]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Axis Layouts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AxisLayout(LayoutBase):
    axis = Vector.property([0,0,0], dtype='3b')

    def layout(self, cells, box, isTrial=False):
        if not cells:
            return box.fromPosSize(box.pos, 0)

        passToken = self.nextPassToken()

        # determin hidden
        visCells = self.cellsVisible(cells)
        axisSizes = self.axisSizesFor(visCells, passToken, box, isTrial)
        lpos, lsize = self.layoutCellsIn(visCells, passToken, axisSizes, box, isTrial)

        return box.fromPosSize(lpos, lsize)

    def axisSizesFor(self, cells, passToken, box, isTrial=False):
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
            axisSizes += weights*availSize/weightSum

        # allow the cells to negotiate space and adjust to it
        axisSizes = self.axisSizeAdjust(cells, passToken, box, weights, axisSizes, isTrial)
        return axisSizes

    def axisSizeAdjust(self, cells, passToken, box, weights, axisSizes, isTrial=False):
        weightSum = weights.sum()

        for x in xrange(self._nAdjustTries):
            # allow cells to adjust for maxsize, rounding, etc
            adjSizes = self.cellsAdjustedSize(cells, passToken, axisSizes, isTrial)
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

            if weightSum <= 0:
                # if there are no more items to reweight, then we are done
                break

            # distributed the available size to the remaining weighted items
            axisSizes += weights*availSize/weightSum

        return axisSizes

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def layoutCellsIn(self, cells, passToken, axisSizes, box, isTrial=False):
        axis = self.axis
        outside = self.outside
        nonAxisSize = (1-axis)*(box.size - outside)
        pos = box.pos + outside
        axisBorders = axis*self.inside

        if isTrial:
            pos += axisSizes.sum(0) + (len(axisSizes)-1)*axisBorders

        else:
            # let each cell know it's new pos and size
            for idx, c in enumerate(cells):
                c.layoutIn(pos.copy(), axisSizes[idx] + nonAxisSize, passToken)
                pos += axisSizes[idx] + axisBorders
            pos -= axisBorders

        lPos = box.pos
        lSize = pos + axis*outside + nonAxisSize
        return lPos, lSize

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def cellsStats(self, cells):
        axis = self.axis
        minSizes = []
        weights = []
        for c in cells:
            weights.append(c.weight * axis)
            minSizes.append(c.minSize * axis)
        return (vstack(weights), vstack(minSizes))

    def cellsAdjustedSize(self, cells, passToken, axisSizes, isTrial=False):
        adjSizes = []
        axis = self.axis
        for c, asize in zip(cells, axisSizes):
            adjSizes.append(asize - c.adjustAxisSize(asize.copy(), axis, passToken, isTrial))
        return vstack(adjSizes)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HLayout(AxisLayout):
    axis = [1,0,0]
class VLayout(AxisLayout):
    axis = [0,1,0]
class DLayout(AxisLayout):
    axis = [0,0,1]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    from uiLayoutCells import *
    cells = [
        Cell(0, 400),
        MaxSizeCell(1, 400, 300),
        Cell(1, 400),
        ]

    vl = VLayout()
    vl.inside.set(10)
    vl.outside.set((50, 50, 0))

    box = Rect.fromPosSize((0,0), (1000, 1000))
    if 1:
        for p in xrange(4):
            if p:
                box.size[:2] = 1000 + (p>>1)*200
            lb = vl.layout(cells, box, not p&1)
            print
            print 'box:', box
            print '  layout:', lb
            for i, c in enumerate(cells):
                print '    cell %s:' % i, c.box
            print

    # timing analysis
    if 0:
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

