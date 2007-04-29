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

from TG.metaObserving import ObserverSet, OBFactoryMap
from TG.kvObserving import KVObject, KVProperty, KVList

from TG.geomath.data.kvBox import KVBox
from TG.geomath.data.vector import Vector
from TG.geomath import layouts

from TG.helix.actors.base import HelixObject

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Layout Cell
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiCell(layouts.LayoutCell):
    oset = ObserverSet.property()
    host = None

    weight = Vector.property([0,0], 'f')
    minSize = Vector.property([0,0], 'f')

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
        else: host.box.pv = lbox.pv

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
            host.box.aspectAt[at] = aspect
        return self

    def fill(self, inset=0):
        @self.on
        def placeFill(host, lbox):
            host.box.pv = lbox.pv
            host.box.inset(inset)
        return self

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

    cell = KVProperty(None)
    strategy = KVProperty(None)
    collection = KVProperty(KVList)
    box = KVProperty(KVBox) # using this form, 

    def __init__(self, kind='abs'):
        self.setKind(kind)

        cell = self.getLayoutCell()
        cell.oset.add(self.performLayout)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getLayoutCell(self, create=True):
        cell = self.cell
        if not create:
            return cell

        if cell is None:
            cell = self._fm_.Cell(self.asWeakRef())
            self.cell = cell

        return cell

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

    def performLayout(self, lbox=None):
        self.strategy.layoutCells(self.collection, self.box)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def add(self, item):
        cell = item.getLayoutCell()
        self.collection.append(cell)
        return cell

    def remove(self, item):
        cell = item.getLayoutCell(False)
        if cell in self.collection:
            self.collection.remove(cell)
            return cell
        return None

    def clear(self, collection):
        self.collection[:] = []

