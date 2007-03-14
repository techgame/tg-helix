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

from basicLayout import BaseLayoutStrategy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Simplest of all layouts... just tell each cell to "deal with it"
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AbsLayoutStrategy(BaseLayoutStrategy):
    """AbsLayout just lets each cell know it should lay itself out"""

    def layout(self, cells, box, isTrial=False):
        box = box.copy()

        self.adjustBox(box)

        # determin visible cells
        visCells = self.cellsVisible(cells)

        if not isTrial:
            for c in cells:
                c.layoutInBox(box)

        return box

    def adjustBox(self, box):
        borders = self.outside
        if borders.any():
            box.pos[:] += borders
            box.size[:] -= 2*borders

