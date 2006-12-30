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
#from numpy import 

from TG.openGL.data import Rect, Vector
from uiLayout import LayoutBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GridLayout(LayoutBase):
    gridCells = Vector.property((4, 2, 1), dtype='3b')

    _haxis = numpy.array([1,0,0], 'b')
    _vaxis = numpy.array([0,1,0], 'b')
    _daxis = numpy.array([0,0,1], 'b')

    def layout(self, cells, box, isTrial=False):
        if not cells:
            return box.fromPosSize(box.pos, 0)

        iCells = iter(cells)
        for b, c in izip(self.iterGridCellBoxes(box, isTrial), iCells):
            c.layoutIn(b[0], b[1])

        for c in iCells:
            c.layoutHide()
        return box.copy()
        
    def iterGridCellBoxes(self, box, isTrial=False):
        gridCells = self.gridCells
        borders = 2*self.outside + (gridCells-1)*self.inside

        availSize = box.size - borders
        cellSize = availSize / gridCells

        posStart = box.pos + box.size*self._vaxis
        # come right and down by the outside border
        posStart += self.outside*(1,-1,0) 
        # come down by one cell height
        posStart += -self._vaxis*cellSize

        advSize = (cellSize + self.inside)
        advCol = self._haxis*advSize
        advRow = -self._vaxis*advSize

        gridCells = self.gridCells
        posRow = posStart.copy()
        for row in xrange(gridCells[1]):
            posCol = posRow.copy()
            for col in xrange(gridCells[0]):
                yield posCol.copy(), cellSize.copy()
                posCol += advCol
            posRow += advRow

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    from uiLayoutCells import *
    cells = [Cell() for i in xrange(10)]

    vl = GridLayout()
    vl.inside.set(10)
    vl.outside.set((50, 50, 0))

    box = Rect.fromPosSize((0,0), (1000, 1000))
    if 1:
        lb = vl.layout(cells, box)
        print
        print 'box:', box
        print '  layout:', lb
        for i, c in enumerate(cells):
            print '    cell %s:' % i, c.box
        print

