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

from itertools import izip
import numpy
from numpy import zeros, ndindex, outer

from TG.openGL.data import Rect, Vector
from uiLayout import LayoutBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GridLayout(LayoutBase):
    gridCells = (3, 4)

    _haxis = numpy.array([1,0,0], 'b')
    _vaxis = numpy.array([0,1,0], 'b')
    _daxis = numpy.array([0,0,1], 'b')

    def layout(self, cells, box, isTrial=False):
        if not cells:
            return box.fromPosSize(box.pos, 0)

        visCells = self.cellsVisible(cells)

        # figure out what our row and column sizes should be from the cells
        rowSizes, colSizes = self.rowColSizesFor(cells, box, isTrial)

        iCells = iter(visCells)
        iCellBoxes = self.iterCellBoxes(visCells, box, rowSizes, colSizes, isTrial)

        # let cells lay themselves out in their boxes
        for (cellPos, cellSize), c in izip(iCellBoxes, iCells):
            c.layoutIn(cellPos, cellSize)

        # hide cells that have no box
        for c in iCells:
            c.layoutHide()

        return box.copy()
        
    def iterCellBoxes(self, cells, box, rowSizes, colSizes, isTrial=False):
        posStart = box.pos + box.size*self._vaxis
        # come right and down by the outside border
        posStart += self.outside*(1,-1,0) 
        advCol = self._haxis*self.inside
        advRow = self._vaxis*self.inside

        posRow = posStart.copy()
        for row in rowSizes:
            # adv down by row
            posRow -= row

            posCol = posRow.copy()
            for col in colSizes:
                # yield cell box
                yield posCol.copy(), row + col

                # adv right by col + inside border
                posCol += col + advCol

            # adv down by inside border
            posRow -= advRow

    def rowColSizesFor(self, cells, box, isTrial=False):
        vaxis = self._vaxis; haxis = self._haxis
        nRows, nCols = self.gridCells

        # figure out how much room the borders take
        borders = 2*self.outside + (nCols-1, nRows-1, 0)*self.inside

        # figure out what our starting size minus borders is
        availSize = box.size - borders 
        cellSize = (availSize / (nCols, nRows, 1)).reshape((1,3))

        # repeat rowSize nRows times
        rowSizes = (cellSize*vaxis).repeat(nRows, 0)
        # repeat colSize nCols times
        colSizes = (cellSize*haxis).repeat(nCols, 0)
        return rowSizes, colSizes

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FlexGridLayout(GridLayout):
    def rowColSizesFor(self, cells, box, isTrial=False):
        vaxis = self._vaxis; haxis = self._haxis
        nRows, nCols = self.gridCells

        # determin weights and sizes for rows and columns
        weights, minSizes = self.cellsStats(cells)

        rowWeights = (vaxis*weights).max(1)
        rowMinSizes = (vaxis*minSizes).max(1)

        colWeights = (haxis*weights).max(0)
        colMinSizes = (haxis*minSizes).max(0)

        rowSizes = rowMinSizes.copy()
        colSizes = colMinSizes.copy()

        # figure out how much room the borders take
        borders = 2*self.outside + (nCols-1, nRows-1, 0)*self.inside

        # figure out what our starting size minus borders is
        availSize = box.size - borders 

        # subtract the already allocated minsize
        availSize -= rowMinSizes.sum(0) + colMinSizes.sum(0)

        if (availSize > 0).any():
            if (availSize*vaxis > 0).any():
                rowWeightSum = rowWeights.sum()
                if (rowWeightSum > 0):
                    # distribute weights across rows
                    rowAdj = availSize*rowWeights/rowWeightSum
                else:
                    # distribute evenly across rows
                    rowAdj = vaxis*availSize/nRows

                rowSizes += rowAdj

            if (availSize*haxis > 0).any():
                colWeightSum = colWeights.sum()
                if (colWeightSum > 0):
                    # distribute weights across columns
                    colAdj = availSize*colWeights/colWeightSum
                else:
                    # distribute evenly across columns
                    colAdj = haxis*availSize/nCols

                colSizes += colAdj

        return rowSizes, colSizes

    def cellsStats(self, cells):
        gridCells = self.gridCells

        nRows, nCols = gridCells[:2]
        minSizes = zeros((nRows, nCols, 3), 'f')
        weights = zeros((nRows, nCols, 3), 'f')

        # grab cell info into minSize and weights arrays
        idxWalk = ndindex(weights.shape[:-1])
        for c, idx in izip(cells, idxWalk):
            minSizes[idx] = c.minSize
            weights[idx] = c.weight

        return weights, minSizes

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    from uiLayoutCells import *
    
    if 1: gl = FlexGridLayout()
    else: gl = GridLayout()

    if 1: cells = [Cell((i%2, (i//4)%2), (100, 100)) for i in xrange(16)]
    else: cells = [Cell() for i in xrange(16)]

    if 1:
        gl.inside.set(10)
        gl.outside.set((50, 50, 0))

    box = Rect.fromPosSize((0,0), (1000, 1000))
    if 1:
        lb = gl.layout(cells, box)
        print
        print 'box:', box
        print '  layout:', lb
        for i, c in enumerate(cells):
            print '    cell %s:' % i, c.box
        print

