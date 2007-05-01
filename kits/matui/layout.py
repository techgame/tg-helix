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

class MatuiCell(layouts.LayoutCell):
    _fm_ = OBFactoryMap(Layout = None)
    oset = OBSet.property()
    host = None

    weight = Vector.property([0,0], 'f')
    minSize = Vector.property([0,0], 'f')

    def __init__(self, host):
        self.host = host

    def set(self, *args, **kw):
        for n,v in args:
            setattr(self, n, v)
        for n,v in kw.items():
            setattr(self, n, v)
        return self

    def getLayoutCell(self, create=False):
        return self

    def layoutInBox(self, lbox):
        host = self.host()
        placeFn = self.placeFn
        if placeFn is not None:
            placeFn(host, lbox)
        else:
            host.box = lbox.copy()

        self.oset.call_n1(lbox)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    placeFn = None
    def onPlace(self, placeFn):
        self.placeFn = placeFn
        return placeFn
    on = onPlace

    def align(self, at0=0.5, at1=None, offset=0):
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

    def newLayout(self, kind='abs'):
        return self._fm_.Layout(kind)
    def addLayout(self, kind='abs'):
        layout = self.newLayout(kind)
        layout.parentCell = self
        return layout
    def removeLayout(self, layout):
        if layout.parentCell is self:
            layout.parentCell = None

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

    def __init__(self, kind='abs'):
        self.setKind(kind)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _kind = None
    def getKind(self):
        return self._kind
    def setKind(self, kind):
        if kind == self._kind: return

        self._kind = kind
        factory = self._fm_.StrategyMap[kind]
        self.strategy = factory()
    kind = property(getKind, setKind)

    def watchBox(self, box):
        self.box.viewOf(box, dim=2)
        self.kvo('box.*', lambda self, box: self.layout())

    _parentCell = None
    def getParentCell(self):
        return self._parentCell
    def setParentCell(self, parentCell):
        lastParentCell = self.getParentCell()
        if lastParentCell is not None:
            lastParentCell.oset.discard(self)
        self._parentCell = parentCell
        if parentCell is not None:
            parentCell.oset.add(self)
    parentCell = property(getParentCell, setParentCell)

    def layout(self, lbox=None):
        if lbox is not None:
            self.box.pv = lbox.pv[..., :2]

        self.strategy(self.collection, self.box)
    __call__ = layout

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add(self, item):
        itemCell = item.getLayoutCell()
        self.collection.append(itemCell)
        return itemCell

    def remove(self, item):
        itemCell = item.getLayoutCell(False)
        if itemCell in self.collection:
            self.collection.remove(itemCell)
            return itemCell
        return None

    def clear(self, collection):
        self.collection[:] = []

MatuiCell._fm_.update(Layout = MatuiLayout)
