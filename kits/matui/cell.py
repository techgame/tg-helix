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

from TG.geomath.data.vector import Vector
from TG.geomath.layouts import LayoutCell

from TG.helix.actors.base import HelixObject

from .layout import MatuiLayout

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Layout Cell
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiCell(HelixObject, LayoutCell):
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
        box.kvo('*', self.layoutInWatchBox)

    def layoutInWatchBox(self, lbox, k='*'):
        self.layoutInBox(lbox)

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

MatuiLayout._fm_.update(Cell = MatuiCell)
MatuiCell._fm_.update(Layout = MatuiLayout)

