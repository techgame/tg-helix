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
from TG.openGL.raw import gl
from TG.openGL import data as glData
from TG.openGL.data import texture
from .uiViewBase import UIView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GLDataView(UIView):
    viewForKeys = []

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ColorView(GLDataView):
    viewForKeys = [glData.ColorArray]

    def init(self, color):
        GLDataView.init(self, None)
        self.updateColor(color)

    def updateColor(self, color):
        self.color = color
        if color:
            im = color.glinfo.glImmediateFor(color)
            self.glColorV = partial(im, color.ctypes.data_as(im.api.argtypes[0]))
        else:
            self.glColorV = lambda: None

    def render(self):
        GLDataView.render(self)

        self.glColorV()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GeometryView(GLDataView):
    viewForKeys = [glData.DataArrayBase]

    def init(self, geom):
        GLDataView.init(self, None)
        self.updateGeom(geom)

    def updateGeom(self, geom):
        self.geom = geom
        if geom is None:
            return False

        self.glArrEnable = partial(
                geom.glinfo.glEnableArray, 
                geom.glinfo.glKindId)
        self.glArrPtr = partial(
                geom.glinfo.glArrayPointer, 
                geom.shape[-1],
                geom.glTypeId,
                geom.strides[-1]*geom.shape[-1],
                geom.ctypes.data_as(geom.glinfo.glArrayPointer.api.argtypes[-1]))
        return True

    def render(self):
        GLDataView.render(self)

        geom = self.geom
        if geom is None: 
            return False

        self.glArrEnable()
        self.glArrPtr()
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BoxView(GeometryView):
    viewForKeys = [glData.Rect]
    vertexScale = glData.VertexArray([[0., 0., 1.], [1., 0., 0.], [1., 1., 0.], [0., 1., 1.]], '3f')

    def init(self, aBox):
        GeometryView.init(self, None)
        aBox._pub_.add(self._onBoxChange)
        self.enqueue(self.updateBox, aBox)

    def updateBox(self, aBox):
        geom = aBox.pos + aBox.size*self.vertexScale
        self.updateGeom(geom)

    def updateGeom(self, geom):
        if not GeometryView.updateGeom(self, geom):
            return False

        count = (geom.size/geom.shape[-1])
        self.glArrDraw = partial(
                gl.glDrawArrays, 
                gl.GL_QUADS, 0, count)
        return True

    def _onBoxChange(self, aBox, attrName, info=None):
        self.enqueue(self.updateBox, aBox)

    def render(self):
        if not GeometryView.render(self):
            return False

        self.glArrDraw()
        return True

