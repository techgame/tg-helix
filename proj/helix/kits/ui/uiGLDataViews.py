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
from .uiViewBase import UIView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ColorView(UIView):
    viewForKeys = [glData.ColorArray]

    def init(self, color):
        UIView.init(self, None)
        self.updateColor(color)

    def updateColor(self, color):
        self.color = color
        if color:
            im = color.glinfo.glImmediateFor(color)
            self.glColorV = partial(im, color.ctypes.data_as(im.api.argtypes[0]))
        else:
            self.glColorV = lambda: None

    def render(self):
        UIView.render(self)

        self.glColorV()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GeometryView(UIView):
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BoxView(GeometryView):
    viewForKeys = [glData.Rect]
    sizeScale = glData.VertexArray(
           [[0., 0., 1.],
            [1., 0., 0.],
            [1., 1., 0.],
            [0., 1., 1.]], '3f')


    def init(self, aBox):
        GeometryView.init(self, None)
        aBox._pub_.add(self._onBoxChange)
        self.enqueue(self.updateBox, aBox)

    def updateBox(self, aBox):
        geom = aBox.pos + aBox.size * self.sizeScale
        self.updateGeom(geom)

    def _onBoxChange(self, aBox, key, info=None):
        self.enqueue(self.updateBox, aBox)

