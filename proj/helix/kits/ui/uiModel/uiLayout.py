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

from TG.observing import ObservableObjectWithProp
from TG.openGL.data import Rect, Vector

import numpy
from numpy import vstack, zeros_like

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Layouts
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LayoutBase(ObservableObjectWithProp):
    def layout(self, cells, box):
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
    outsideBorders = Vector.property([0,0,0], dtype='3b')
    insideBorders = Vector.property([0,0,0], dtype='3b')

    nAdjustTries = 3
    _passToken = 0
    def layout(self, cells, box, trial=False):
        passToken = self.nextPassToken()

        # determin hidden
        visCells = self.cellsVisible(cells)
        axisSizes = self.axisSizesFor(visCells, passToken, box)
        fpos, fsize = self.layoutCellsIn(visCells, passToken, axisSizes, box)

        return box.fromPosSize(fpos, fsize)

    def axisSizesFor(self, cells, passToken, box):
        # determin minsize
        axis = self.axis
        weights, minSizes = self.cellsStats(cells)

        borders = axis*(2*self.outsideBorders + (len(cells)-1)*self.insideBorders)
        availSize = axis*box.size - borders - minSizes.sum(0)

        weightSum = weights.sum()
        axisSizes = minSizes + weights*availSize/weightSum

        # allow cells to adjust for maxsize, rounding, etc
        for x in xrange(self.nAdjustTries): # max of ten tries
            adjSizes = self.cellsAdjustedSize(cells, passToken, axisSizes)
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

        return axisSizes

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def cellsStats(self, cells):
        axis = self.axis
        minSizes = []
        weights = []
        for c in cells:
            weights.append(c.weight * axis)
            minSizes.append(c.minSize * axis)
        return (vstack(weights), vstack(minSizes))

    def cellsAdjustedSize(self, cells, passToken, axisSizes):
        adjSizes = []
        for c, asize in zip(cells, axisSizes):
            adjSizes.append(asize - c.adjustAxisSize(asize.copy(), passToken))
        return vstack(adjSizes)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def layoutCellsIn(self, cells, passToken, axisSizes, box):
        axis = self.axis
        outsideBorders = self.outsideBorders
        nonAxisSize = (1-axis)*(box.size - outsideBorders)
        pos = box.pos + outsideBorders
        axisBorders = axis*self.insideBorders

        # let each cell know it's new pos and size
        for idx, c in enumerate(cells):
            c.layoutIn(pos, axisSizes[idx] + nonAxisSize, passToken)
            pos += axisSizes[idx] + axisBorders

        lPos = box.pos
        # track size of all cells, and add the non-axis size to fill out our total size
        lSize = (axisSizes.sum(0) + nonAxisSize)
        # now account for the borders
        lSize += outsideBorders + axis*outsideBorders + (len(cells)-1)*axisBorders
        return lPos, lSize

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
        Cell(0, 100),
        MaxSizeCell(1, 100, 300),
        Cell(1, 100),
        ]

    vl = VLayout()
    vl.insideBorders.set(10)
    vl.outsideBorders.set((50, 50, 0))

    box = Rect.fromPosSize((0,0), (1000, 1000))
    for p in xrange(3):
        lb = vl.layout(cells, box)
        print
        print 'box:', box
        print '  layout:', lb
        for i, c in enumerate(cells):
            print '    cell %s:' % i, c.box
        print

