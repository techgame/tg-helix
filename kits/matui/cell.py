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

from __future__ import with_statement
from numpy import asarray
from TG.metaObserving import OBSet, OBFactoryMap

from TG.geomath.data.box import Box
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
    hostRef = None

    weight = Vector.property([0,0], 'f')
    minSize = Vector.property([0,0], 'f')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, hostRef):
        hostRef()
        self.hostRef = hostRef

    def isLayout(self): return True

    def layout(self):
        self.layoutInBox(self.hostRef().box)

    def layoutInBox(self, lbox):
        if lbox is None:
            self.hide()
            return
        lbox = lbox.copy(dim=2)
        host = self.hostRef()
        if host is not None:
            self._placeFn(host, lbox)
            self.oset.call_n2(self, getattr(host, 'box', lbox))
            self.show()

    def _onBoxChanged(self, host, lbox):
        self.layoutInBox(lbox)

    def watchBox(self, box):
        box.kvo('*', self._onBoxChanged)
    def watchHostBox(self, host):
        host.kvo('box.*', self._onBoxChanged)

    _hidden = False
    def hide(self):
        self._hidden = True
        self.node.enable(False)

    def show(self):
        if self._hidden:
            self._hidden = False
            self.node.enable(True)

    def debug(self, fn=None, **kw):
        if fn is None:
            def dbgPrintLayout(cell, box):
                print '%r box:%r size: %r' % (sorted(kw.items()), box.tolist(), box.size)
            fn = dbgPrintLayout
        return self.oset.on(fn)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Placement methods
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def ignore(self):
        self.on(lambda host, lbox: None)
        return self

    @staticmethod
    def _placeAssign(host, lbox):
        host.box = lbox.copy()
    def assign(self):
        self.on(self._placeAssign)
        return self

    def offset(self, offset=0):
        return self.align(0, 0, offset)

    def dock(self, sw, at0=None, at1=None, offset=0):
        sw = asarray(sw)
        if at0 is None:
            at0 = 1-sw
        if at1 is None: 
            at1 = at0
        @self.on
        def placeDocked(host, lbox):
            hbox = host.box
            with hbox.kvpub:
                hbox.size = (sw)*lbox.size + (1-sw)*hbox.size
                hbox.at[at0] = lbox.at[at1] + offset
        return self

    def align(self, at0=0, at1=None, offset=0):
        if at1 is None: 
            at1 = at0
        @self.on
        def placeAligned(host, lbox):
            host.box.at[at0] = lbox.at[at1] + offset
        return self

    def alignCorners(self, at0=0, at1=1, offset0=0, offset1=0):
        @self.on
        def placeAligned(host, lbox):
            host.box.pv = lbox.at[at0]+offset0, lbox.at[at1]+offset1
        return self

    def aspect(self, aspect, at=.5):
        @self.on
        def placeAspect(host, lbox):
            host.box.atAspect[aspect,at] = lbox
        return self

    def aspectFill(self, at=.5, grow=True, aspect=None):
        @self.on
        def placeFill(host, lbox, aspect=aspect):
            if aspect is None:
                aspect = host.box.size
            with host.box.kvpub:
                host.box.at[at] = lbox.at[at]
                host.box.setAspectWith((aspect, grow), lbox.size)
        return self

    def fillHeight(self, at0=.5, at1=None, offset=0, inset=0):
        if at1 is None: 
            at1 = at0
        if isinstance(inset, (int, float, long)):
            inset = (0, inset)

        @self.on
        def placeFillHeight(host, lbox):
            with host.box.kvpub:
                host.box.height = lbox.height
                host.box.inset(inset)
                host.box.at[at0] = lbox.at[at1] + offset
        return self

    def fillWidth(self, at0=.5, at1=None, offset=0, inset=0):
        if at1 is None: 
            at1 = at0
        if isinstance(inset, (int, float, long)):
            inset = (inset, 0)

        @self.on
        def placeFillWidth(host, lbox):
            with host.box.kvpub:
                host.box.width = lbox.width
                host.box.inset(inset)
                host.box.at[at0] = lbox.at[at1] + offset
        return self

    def fill(self, inset=0, offset=0):
        @self.on
        def placeFill(host, lbox):
            with host.box.kvpub:
                host.box.pv = lbox.pv
                host.box.inset(inset)
                host.box += offset
        return self

    _placeFn = _placeAssign
    def onPlace(self, placeFn):
        self._placeFn = placeFn
        return placeFn
    on = onPlace

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Layout creation
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def newLayout(self, kind='abs', node=None, cell=True):
        return self._fm_.Layout(kind, node, cell)
    def addLayout(self, kind='abs', node=None, cell=None):
        layout = self.newLayout(kind, node, cell)
        layout.watchCell(self, True)
        return layout
    def removeLayout(self, layout):
        layout.watchCell(self, False)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getNode(self):
        host = self.hostRef()
        if host is not None:
            return host.node
    node = property(getNode)

    def getBox(self):
        host = self.hostRef()
        if host is not None:
            return host.box
    box = property(getBox)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Spacer Cell 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

class SpacerCell(HelixObject, LayoutCell):
    weight = Vector.property([0,0], 'f')
    minSize = Vector.property([0,0], 'f')

    box = Box.property(dtype='i')

    def __init__(self, size=None, weight=None):
        if size or weight:
            self.init(size, weight)

    def init(self, size=None, weight=None):
        if size is None: 
            if weight is None:
                raise ValueError("Must specify weight or size, both are currently None")
        elif isinstance(size, (int, long, float)):
            size = (size, size)

        if isinstance(weight, (int, long, float)):
            weight = (weight, weight)
        
        if size is not None:
            self.minSize[:] = size
            self.box.size[:] = size

        if weight is not None:
            self.weight[:] = weight 

        
    def layoutInBox(self, lbox):
        """Called with a Box instance or None when the cell has been placed"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 

MatuiLayout._fm_.update(Cell = MatuiCell, SpacerCell = SpacerCell)
MatuiCell._fm_.update(Layout = MatuiLayout)



