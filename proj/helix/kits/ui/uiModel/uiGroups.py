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

from .uiBase import UIItemWithBox, glData, numpy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIList(UIItemWithBox):
    viewVisitKeys = ["UIList"]

    items = UIItemWithBox.ActorList.property(propKind='astype')

    scale = False
    translate = True

    def __init__(self, items=None, **kwattr):
        super(UIList, self).__init__()
        if kwattr:
            self.set(kwattr)

        if items is not None:
            self.items = items

    @items.fset
    def setItems(self, items, _paSet_):
        _paSet_.fget()[:] = items

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getItemBox(self, items=None):
        if items is None: items = self.items
        return glData.Rect.fromUnion(i.box for i in items if hasattr(i, 'box'))
    itemBox = property(getItemBox)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIComposite(UIList):
    viewVisitKeys = ["UIComposite"]
    scale = True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIGrid(UIComposite):
    viewVisitKeys = ["UIGrid"]

    border = glData.Vector.property([10, 10, 0], dtype='3f')
    def __init__(self, gridItems, gridCells, **kwattr):
        super(UIGrid, self).__init__()
        self.gridCells = gridCells + (1,)

        n = numpy.prod(gridCells)
        self.items = [item for i, item in zip(xrange(n), gridItems)]

        if kwattr:
            self.set(kwattr)

        self._pub_.add(self._onGridUpdate, 'box')
        self.box._pub_.add(self._onGridUpdate)

    def _onGridUpdate(self, item, attr):
        self.layout()

    def layout(self):
        border = self.border
        gridCells = self.gridCells

        gridSize = self.box.size
        fullCellSize = (gridSize - border)/self.gridCells
        cellRect = glData.Rect.fromPosSize(border, fullCellSize - border)

        advRight = (1,0,0)*fullCellSize
        advDown = (0,-1,0)*fullCellSize

        gridTopLeft = (border * (1,-1,0)) + advDown
        gridTopLeft[1] += gridSize[1]

        iterItems = iter(self.items)
        try:
            for row in xrange(gridCells[1]):
                for col in xrange(gridCells[0]):
                    item = iterItems.next()

                    cr = cellRect.copy()
                    cr.pos.set(gridTopLeft + row*advDown + col*advRight)
                    cr.setAspect(item.box.aspect, 0.5)

                    item.boxScale = cr.copy()
        except StopIteration:
            pass

