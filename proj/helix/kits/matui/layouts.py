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

class MatuiLayoutCell(LayoutCell):
    def isMatuiActor(self): 
        return False
    def isMatuiCell(self): 
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _strategy = None
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

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def new(klass, *args, **kw):
        return klass(*args, **kw)

    def addNewLayout(self, *args, **kw):
        layoutCell = self.new(*args, **kw)
        return self.addCell(layoutCell)

    def addNewCell(self, item, *args, **kw):
        if cell is None:
            cell = self.newCell()
        if not cell.isMatuiCell():
            raise ValueError("Expected a matui cell or layout cell")
        self.cells.append(cell)
        return cell

MatuiLayout = MatuiLayoutCell

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Specific cells
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiCell(BasicCell):
    onlayout = None
    def onevt(self, evtfn):
        """Event decorator"""
        self.onlayout = evtfn
        return self #evtfn

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
        if weight:
            self.weight = weight

    def isMatuiActor(self): 
        return False
    def isMatuiCell(self): 
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _actor = None
    def getActor(self):
        return self._actor
    def setActor(self, actor):
        self._actor = actor
        minSize = actor.minSize
        if minSize is not None:
            self.minSize = minSize

        self.maxSize = actor.maxSize
        if self.maxSize is not None:
            self.adjustSize = adjustForMaxSize

        self.onevt(actor.onCellLayout)
    actor = property(getActor, setActor)

