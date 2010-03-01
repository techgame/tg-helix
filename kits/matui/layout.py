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
    collection = KVProperty(KVList)
    box = KVBox.property()
    oset = OBSet.property()

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
            cell = self._fm_.Cell(self.asWeakRef())

        self._cell = cell
        self.watchCell(cell)
    cell = property(getCell, setCell)

    def watchCell(self, cell, watch=True):
        cell.oset.change(watch, lambda cell, lbox: self.layout(lbox))
    def watchHostBox(self, host):
        host.kvo('box.*', lambda host, lbox: self.layout(lbox))

    passCount = 1
    def layout(self, lbox=None):
        box = self.box
        if lbox is not None:
            box.pv = lbox.pv[..., :box.shape[-1]]

        for n in xrange(self.passCount):
            self.alg(self.viewCollection, box)
        self.oset.call_n3(self, 'layout', box)

    def fit(self, at=None):
        box = self.alg.fit(self.viewCollection)
        self.oset.call_n3(self, 'fit', box)
        self.box.setSize(box.size, at=at)
        return box

    def debug(self, fn=None, **kw):
        if fn is None:
            def dbgPrintLayout(layout, op, box):
                print '%r op: %r box:%r size: %r' % (sorted(kw.items()), op, box.tolist(), box.size)
            fn = dbgPrintLayout
        return self.oset.on(fn)

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
        if item is None:
            self.collection.append(None)
            return
        node = kw.pop('node', self._node)
        if not item.isLayout():
            if node is not None:
                node.add(item)
        itemCell = item.cell
        if itemCell is None:
            raise ValueError("Item.cell is None!")
        if kw:
            for k,v in kw.iteritems():
                setattr(itemCell, k, v)
        self.collection.append(itemCell)
        return itemCell
    def addOnly(self, item, **kw):
        itemCell = item.cell
        self.collection.append(itemCell)
        return itemCell

    def addSpacer(self, size=None, weight=None):
        cell = self._fm_.SpacerCell(size, weight)
        self.collection.append(cell)
        return cell


    def remove(self, item, **kw):
        node = kw.pop('node', self._node)
        if not item.isLayout():
            if node is not None:
                node.remove(item)
        itemCell = item.cell
        if itemCell in self.collection:
            self.collection.remove(itemCell)
            return itemCell
        return None

    def assign(self, item, **kw):
        self.clear()
        return self.add(item, **kw)

    def clear(self):
        if self._node is not None:
            self._node.clear()
        self.collection[:] = []
        self.viewCollection = None

    def axisSizes(self, collection=None, incBox=False):
        if collection is None:
            collection = self.collection
        sizes, box = self.alg.axisSizesFor(collection)
        if incBox:
            return sizes, box
        else: return sizes

    def primaryAxisSize(self, collection=None, incAxisIdx=True):
        sizes = self.axisSizes(collection)
        axisIdx = self.alg.axis.argmax()
        if incAxisIdx:
            return axisIdx, sizes[:,axisIdx]
        else:
            return sizes[:,axisIdx]

