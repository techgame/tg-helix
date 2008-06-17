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
from TG.geomath import layouts

from TG.helix.actors.base import HelixObject

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
            Cell = None,
            )

    alg = KVProperty(None)
    cell = KVProperty(None)
    collection = KVProperty(KVList)
    box = KVBox.property()

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
        self.alg = factory()
    kind = property(getKind, setKind)

    _node = None
    def getNode(self):
        return self._node
    def setNode(self, node):
        self._node = node
    node = property(getNode, setNode)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _cell = None
    def getCell(self):
        return self._cell
    def setCell(self, cell):
        if cell is True:
            cell = self._fm_.Cell(self)

        self._cell = cell
        self.watchCell(cell)
    cell = property(getCell, setCell)

    def watchCell(self, cell, watch=True):
        cell.oset.change(watch, lambda cell, lbox: self.layout(lbox))
    def watchHostBox(self, host):
        host.kvo('box.*', lambda host, lbox: self.layout(lbox))

    def layout(self, lbox=None):
        box = self.box
        if lbox is not None:
            box.pv = lbox.pv[..., :box.shape[-1]]

        self.alg(self.viewCollection, box)

    def fit(self):
        box = self.alg.fit(self.viewCollection, self.box)
        self.box.size = box.size
        return box

    _viewCollection = None
    def getViewCollection(self):
        if self._viewCollection is None:
            return self.collection
        return self._viewCollection
    def setViewCollection(self, viewCollection):
        self._viewCollection = viewCollection
    def delViewCollection(self):
        del self._viewCollection
    viewCollection = property(getViewCollection, setViewCollection, delViewCollection)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __iadd__(self, other):
        self.add(other)
        return self
    def __isub__(self, other):
        self.remove(other)
        return self

    def add(self, item, **kw):
        if not item.isLayout() and self._node is not None:
            self._node.add(item)
        itemCell = item.cell
        if kw:
            for k,v in kw.iteritems():
                setattr(itemCell, k, v)
        self.collection.append(itemCell)
        return itemCell
    def addOnly(self, item, **kw):
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
        self.viewCollection = None

