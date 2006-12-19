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

from .uiBase import UIItem, glData, numpy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIList(UIItem):
    viewVisitKeys = ["UIList"]

    items = UIItem.ActorList.property()
    box = glData.Rectf.property()

    def __init__(self, items, **kwattr):
        if kwattr:
            self.set(kwattr)
        self.items[:] = items
        self.items._pub_.add(self._onItemsChange)

        self.calcBox()

    def _onItemsChange(self, items, attr):
        self.calcBox()

    def calcBox(self):
        pos = numpy.vstack(i.box.pos for i in self.items if hasattr(i, 'box')).min(0)
        corner = numpy.vstack(i.box.corner for i in self.items if hasattr(i, 'box')).max(0)
        box = glData.Rectf.fromCorners(pos, corner)
        self.box = box
        return box

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIComposite(UIItem):
    viewVisitKeys = ["UIComposite"]
    items = UIItem.ActorList.property()

    box = glData.Rectf.property()
    boxComp = glData.Rectf.property()

    def getPos(self): return self.box.pos
    def setPos(self, pos): self.box.pos.set(pos)
    pos = property(getPos, setPos)

    def getSize(self): return self.box.size
    def setSize(self, size): self.box.size.set(size)
    size = property(getSize, setSize)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIGrid(UIComposite):
    border = glData.Vector.property([10, 10, 0], dtype='3f')
    def __init__(self, gridItems, gridCells, **kwattr):
        super(UIGrid, self).__init__()
        self.gridItems = gridItems
        self.gridCells = gridCells

        if kwattr:
            self.set(kwattr)

        self._pub_.add(self._onGridUpdate)
        self.box._pub_.add(self._onGridUpdate, 'size')
        self.boxComp.size = self.box.size

    def _onGridUpdate(self, item, attr):
        self.layout()

    def layout(self):
        border = self.border
        gridCells = self.gridCells

        fullCellSize = (self.boxComp.size[:2] - border[:2])/self.gridCells
        cellRect = glData.Rect.fromPosSize(border, fullCellSize - border[:2])

        fullCellRect = glData.Rect.fromSize(fullCellSize)
        advRight = fullCellRect.at((1,0,0))
        advDown = -fullCellRect.at((0,1,0))

        gridTopLeft = self.boxComp.at((0, 1, 0)) + (border * (1, -1, 0)) + advDown

        gridItems = []
        iterItems = iter(self.gridItems)
        try:
            for row in xrange(gridCells[1]):
                for col in xrange(gridCells[0]):
                    item = iterItems.next()
                    cellRect.pos.set(gridTopLeft + row*advDown + col*advRight)
                    item.box.setRect(cellRect, item.box.aspect, 0.5)
                    gridItems.append(item)
        except StopIteration:
            pass

        self.items[:] = gridItems

