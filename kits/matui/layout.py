##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2007  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.metaObserving import OBSet, OBFactoryMap
from TG.kvObserving import KVObject, KVProperty, KVList

from TG.geomath.data.kvBox import KVBox
from TG.geomath.data.vector import Vector
from TG.geomath import layouts

from TG.helix.actors.base import HelixObject

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Layout Cell
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiCell(HelixObject, layouts.LayoutCell):
    _fm_ = OBFactoryMap(Layout = None)
    oset = OBSet.property()
    host = None

    weight = Vector.property([0,0], 'f')
    minSize = Vector.property([0,0], 'f')

    def __init__(self, host):
        self.host = host

    def isLayout(self): return True

    def set(self, *args, **kw):
        for n,v in args:
            setattr(self, n, v)
        for n,v in kw.items():
            setattr(self, n, v)
        return self

    def getLayoutCell(self):
        return self
    cell = property(getLayoutCell)

    def watchBox(self, box):
        box.kvo('*', self.layoutInBox)

    def layoutInBox(self, lbox, k='*'):
        lbox = lbox.copy(dim=2)
        host = self.host
        placeFn = self.placeFn
        if placeFn is not None:
            placeFn(host, lbox)
        else:
            host.box = lbox.copy()

        self.oset.call_n2(self, getattr(host, 'box', lbox))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    placeFn = None
    def onPlace(self, placeFn):
        self.placeFn = placeFn
        return placeFn
    on = onPlace

    def offset(self, offset=0):
        return self.align(0, 0, offset)
    def align(self, at0=0, at1=None, offset=0):
        if at1 is None: 
            at1 = at0

        @self.on
        def placeAligned(host, lbox):
            host.box.at[at0] = lbox.at[at1] + offset
        return self

    def aspect(self, aspect, at=.5):
        @self.on
        def placeAspect(host, lbox):
            host.box.atAspect[aspect,at] = lbox
        return self

    def fill(self, inset=0):
        @self.on
        def placeFill(host, lbox):
            host.box.pv = lbox.pv
            host.box.inset(inset)
        return self

    def newLayout(self, kind='abs', node=None, cell=True):
        return self._fm_.Layout(kind, node, cell)
    def addLayout(self, kind='abs', node=None, cell=None):
        layout = self.newLayout(kind, node, cell)
        layout.watchCell(self)
        return layout
    def removeLayout(self, layout):
        layout.watchCell(self, False)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Layout Object
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

StrategyFactoryMap = {
    'abs': layouts.AbsLayoutStrategy,

    'vert': layouts.VerticalLayoutStrategy,
    'vertical': layouts.VerticalLayoutStrategy,

    'horiz': layouts.HorizontalLayoutStrategy,
    'horizontal': layouts.HorizontalLayoutStrategy,

    'grid': layouts.GridLayoutStrategy,
    'flex': layouts.FlexGridLayoutStrategy,
    }


class MatuiLayout(HelixObject, KVObject):
    _fm_ = OBFactoryMap(
            StrategyMap = StrategyFactoryMap,
            Cell= MatuiCell,
            )

    strategy = KVProperty(None)
    collection = KVProperty(KVList)
    box = KVBox.property()
    cell = None

    def __init__(self, kind='abs', node=None, cell=None):
        self.setKind(kind)
        if node is not None:
            self.setNode(node)
        if cell is not None:
            self.setCell(cell)

    def isLayout(self): return True

    _kind = None
    def getKind(self):
        return self._kind
    def setKind(self, kind):
        if kind == self._kind: return

        self._kind = kind
        factory = self._fm_.StrategyMap[kind]
        self.strategy = factory()
    kind = property(getKind, setKind)

    _node = None
    def getNode(self):
        return self._node
    def setNode(self, node):
        self._node = node
    node = property(getNode, setNode)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setCell(self, cell):
        if cell is True:
            cell = self._fm_.Cell(self)

        self.watchCell(cell)
        self.cell = cell

    def watchCell(self, cell, watch=True):
        cell.oset.change(watch, self.onWatchedCellNotify)

    def onWatchedCellNotify(self, wcell, lbox):
        self.layout(lbox)

    def layout(self, lbox=None):
        if lbox is not None:
            self.box.pv = lbox.pv[..., :2]

        self.strategy(self.collection, self.box)

    def fit(self):
        box = self.strategy.fit(self.collection, self.box)
        self.box.size = box.size

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add(self, item):
        if not item.isLayout() and self._node is not None:
            self._node.add(item)
        itemCell = item.cell
        self.collection.append(itemCell)
        return itemCell

    def remove(self, item):
        if not item.isLayout() and self._node is not None:
            self._node.remove(item)
        itemCell = item.cell
        if itemCell in self.collection:
            self.collection.remove(itemCell)
            return itemCell
        return None

    def clear(self):
        if self._node is not None:
            self._node.clear()
        self.collection[:] = []

MatuiCell._fm_.update(Layout = MatuiLayout)

