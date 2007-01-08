##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

__all__ = []

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.openGL.layouts.cells import BasicCell, adjustForMaxSize
from TG.openGL.layouts.cellLayout import LayoutCell

from TG.openGL.layouts.absLayout import AbsLayoutStrategy
from TG.openGL.layouts.axisLayout import AxisLayoutStrategy, VerticalLayoutStrategy, HorizontalLayoutStrategy
from TG.openGL.layouts.gridLayout import GridLayoutStrategy
from TG.openGL.layouts.flexGridLayout import FlexGridLayoutStrategy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

strategyFactoryMap = {
    'absolute': AbsLayoutStrategy,
    'abs': AbsLayoutStrategy,

    'axis': AxisLayoutStrategy,

    'horizontal': HorizontalLayoutStrategy,
    'horiz': HorizontalLayoutStrategy,

    'vertical': VerticalLayoutStrategy,
    'vert': VerticalLayoutStrategy,

    'grid': GridLayoutStrategy,

    'flexgrid': FlexGridLayoutStrategy,
    }

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiCellMixin(object):
    def isMatuiNode(self): return False
    def isMatuiActor(self): return False
    def isMatuiCell(self): return True
    def isMatuiLayout(self): return False

    onlayout = None
    def onevt(self, evtfn):
        """Event decorator"""
        self.onlayout = evtfn
        return self #evtfn

    def __repr__(self):
        return '%s' % (self.__class__.__name__, )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiLayoutCell(LayoutCell, MatuiCellMixin):
    def __init__(self, strategy=None, cells=None):
        super(MatuiLayoutCell, self).__init__(strategy, cells)

    def isMatuiLayout(self): return True

    def __repr__(self):
        return '%s|%s|' % (self.__class__.__name__, len(self.cells))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _strategy = AbsLayoutStrategy()
    def getStrategy(self):
        return self._strategy
    def setStrategy(self, strategy, *args, **kw):
        if isinstance(strategy, str):
            self.loadStrategyByKey(strategy, *args, **kw)
        else: self._strategy = strategy
        return self
    strategy = property(getStrategy, setStrategy)

    strategyFactoryMap = strategyFactoryMap
    def loadStrategyByKey(self, strategyKey, *args, **kw):
        strategyFactory = self.strategyFactoryMap[strategyKey]
        strategy = strategyFactory(*args, **kw)
        self.setStrategy(strategy)
        return strategy

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @classmethod
    def new(klass, *args, **kw):
        return klass(*args, **kw)

    @classmethod
    def newLayoutForActor(klass, actor, *args, **kw):
        self = klass.new(*args, **kw)
        return self

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def itemAsCell(self, item):
        isMatuiCell = getattr(item, 'isMatuiCell', lambda: False)
        if isMatuiCell():
            return item
        isMatuiActor = getattr(item, 'isMatuiActor', lambda: False)
        if isMatuiActor():
            return item.asCellForHost(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addNewLayout(self, *args, **kw):
        layoutCell = self.new(*args, **kw)
        return self.addCell(layoutCell)

    def addNewCell(self, item, *args, **kw):
        if cell is None:
            cell = self.newCell()

        return self.addCell(cell)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Layout collection protocol
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __iadd__(self, other):
        self.add(other)
        return self
    def __isub__(self, other):
        self.remove(other)
        return self

    def insert(self, idx, item):
        cell = self.itemAsCell(item)
        if cell is None:
            for each in item:
                self.insert(idx, each)
                idx += 1 # advance the index as we add items
            return self

        return self.insertCell(idx, cell)

    def add(self, item):
        cell = self.itemAsCell(item)
        if cell is None:
            for each in item:
                self.add(each)
            return self

        return self.addCell(cell)

    def remove(self, item):
        isMatuiCell = getattr(item, 'isMatuiCell', lambda: False)
        if isMatuiCell():
            return self.removeCell(item)

        for each in item:
            self.remove(each)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addCell(self, cell):
        self.cells.append(cell)
        return cell
    def insertCell(self, idx, cell):
        self.cells.insert(idx, cell)
        return cell
    def removeCell(self, cell):
        self.cells.remove(cell)
        return cell

MatuiLayout = MatuiLayoutCell

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Specific cells
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiCell(BasicCell, MatuiCellMixin):
    def __call__(self, *args, **kw):
        return self.onlayout(self, self.box, *args, **kw)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiEventCell(MatuiCell):
    def __init__(self, evtfn=None, _info_={}, **kwinfo):
        if evtfn is not None:
            self.onevt(evtfn)

        self.info = kwinfo
        self.info.update(_info_)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiActorCell(MatuiCell):
    weight = 0
    minSize = None
    maxSize = None

    def __init__(self, actor, weight=0):
        if actor is not None:
            self.actor = actor
        if weight:
            self.weight = weight

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _actor = None
    def getActor(self):
        return self._actor
    def setActor(self, actor):
        self._actor = actor
        minSize = getattr(actor, 'minSize', None)
        if minSize is not None:
            self.minSize = minSize

        self.maxSize = getattr(actor, 'maxSize', None)
        if self.maxSize is not None:
            self.adjustSize = adjustForMaxSize

        self.onevt(getattr(actor, 'onCellLayout', None))
    actor = property(getActor, setActor)

