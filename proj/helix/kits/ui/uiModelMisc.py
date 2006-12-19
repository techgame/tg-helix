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

from .uiModelBase import UIItem, glData, numpy

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Viewport settings
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIViewport(UIItem):
    viewVisitKeys = ["UIViewport"]

    box = glData.Recti.property()

    def onViewResize(self, viewSize):
        self.box.size.set(viewSize)

class UIOrthoViewport(UIViewport):
    viewVisitKeys = ["UIOrthoViewport"]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIBlend(UIItem):
    viewVisitKeys = ["UIBlend"]
    flyweights = {
        }
    def __new__(klass, mode):
        self = klass.flyweights.get(mode, None)
        if self is None:
            self = UIItem.__new__(klass, mode)
        return self

    def __init__(self, mode):
        self._mode = mode
        self.flyweights[mode] = self

    _mode = None
    def getMode(self):
        return self._mode
    mode = property(getMode)

