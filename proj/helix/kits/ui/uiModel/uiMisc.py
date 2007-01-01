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

from .uiBase import UIItem, UIItemWithBox, glData, numpy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Viewports
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIViewport(UIItemWithBox):
    viewVisitKeys = ["UIViewport"]

    box = glData.Recti.property()

    def onViewResize(self, viewSize):
        self.box.size = viewSize

class UIOrthoViewport(UIViewport):
    viewVisitKeys = ["UIOrthoViewport"]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Blending
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIBlend(UIItem):
    viewVisitKeys = ["UIBlend"]
    flyweights = {}

    def __new__(klass, mode=None):
        self = klass.flyweights.get(mode, None)
        if self is None:
            self = super(UIItem, klass).__new__(klass, mode)
            self.flyweights[mode] = self
        return self

    def __init__(self, mode=None):
        if mode is not None:
            self._mode = mode

    _mode = None
    def getMode(self):
        return self._mode
    mode = property(getMode)
UIBlend.flyweights[None] = UIBlend('blend')
assert UIBlend().mode == 'blend'

