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

from functools import partial
import numpy
from TG.openGL import data as glData
from TG.openGL.raw import gl
from .uiViewBase import UIView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Widget Views
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ColorView(UIView):
    viewForKeys = [glData.ColorArray]

    def init(self, color):
        UIView.init(self, None)
        self.updateColor(color)

    def updateColor(self, color):
        self.color = color
        im = color.glinfo.glImmediateFor(color)
        self.glColorV = partial(im, color.ctypes.data_as(im.api.argtypes[0]))

    def render(self):
        UIView.render(self)

        self.glColorV()

class VertexView(UIView):
    viewForKeys = [glData.VertexArray]

    def init(self, geom):
        UIView.init(self, None)
        self.updateGeom(geom)

    def updateGeom(self, geom):
        self.geom = geom
        if geom is None:
            return

        arrPtr = geom.glinfo.glArrayPointer
        self.glArrPtr = partial(arrPtr, 
                geom.shape[-1],
                geom.glTypeId,
                geom.strides[-1]*geom.shape[-1],
                geom.ctypes.data_as(arrPtr.api.argtypes[-1]))

    def render(self):
        UIView.render(self)

        geom = self.geom
        if geom is None: return

        gl.glEnableClientState(geom.glinfo.glKindId)
        self.glArrPtr()
        count = (geom.size/geom.shape[-1])
        gl.glDrawArrays(gl.GL_QUADS, 0, count)

class BoxView(VertexView):
    viewForKeys = [glData.Rect]
    sizeScale = glData.VertexArray(
           [[0., 0., 1.],
            [1., 0., 0.],
            [1., 1., 0.],
            [0., 1., 1.]], '3f')


    def init(self, aBox):
        VertexView.init(self, None)
        aBox._pub_.add(self._onBoxChange)
        self.enqueue(self.updateBox, aBox)

    def updateBox(self, aBox):
        geom = aBox.pos + aBox.size * self.sizeScale
        self.updateGeom(geom)

    def _onBoxChange(self, aBox, key, info=None):
        self.enqueue(self.updateBox, aBox)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class WidgetView(UIView):
    viewForKeys = ['Widget']

    def init(self, widget):
        UIView.init(self, widget)
        self.updateWidget(widget)

    def _onViewableChange(self, viewable, attr, info=None):
        UIView._onViewableChange(self, viewable, attr, info=None)

        if attr in ('color', 'box'):
            self.updateWidget(viewable)

    def updateWidget(self, widget):
        self.parts = self.viewListFor([widget.color, widget.box])

    def render(self):
        UIView.render(self)
        for p in self.parts:
            p.render()

