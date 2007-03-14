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
from numpy import zeros_like, zeros, empty_like, empty, ndindex

from ..data import Rect, Vector
from .gridLayout import GridLayoutStrategy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FlexGridLayoutStrategy(GridLayoutStrategy):
    def rowColSizesFor(self, cells, box, isTrial=False):
        vaxis = self._vaxis; haxis = self._haxis
        nRows = self.nRows; nCols = self.nCols

        # determin weights and sizes for rows and columns
        weights, minSizes = self.cellsStats(cells)

        rowWeights = vaxis*weights.max(1)
        rowSizes = vaxis*minSizes.max(1)

        colWeights = haxis*weights.max(0)
        colSizes = haxis*minSizes.max(0)

        # figure out how much room the borders take
        borders = 2*self.outside + (nCols-1, nRows-1)*self.inside

        gridMinSize = borders + rowSizes.sum(0) + colSizes.sum(0)
        box.size[:] = numpy.max([box.size, gridMinSize], 0)

        # figure out what our starting size minus borders is
        availSize = box.size - gridMinSize

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

    def cellsStats(self, cells, default=zeros((2,), 'f')):
        nRows = self.nRows; nCols = self.nCols
        minSizes = empty((nRows, nCols, 2), 'f')
        weights = empty((nRows, nCols, 2), 'f')

        # grab cell info into minSize and weights arrays
        idxWalk = ndindex(weights.shape[:-1])
        for c, idx in izip(cells, idxWalk):
            weights[idx] = (getattr(c, 'weight', None) or default)
            minSizes[idx] = (getattr(c, 'minSize', None) or default)

        return weights, minSizes

