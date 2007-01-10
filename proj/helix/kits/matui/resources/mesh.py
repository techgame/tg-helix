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

import numpy

from TG.openGL import data as glData
from TG.openGL.data.bufferObjects import ArrayBuffer

from .units import MatuiLoaderMixin, MatuiMeshUnit

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Loader Mixin
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MeshLoaderMixin(MatuiLoaderMixin):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Mesh Resources
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Immediate(MatuiMeshUnit):
    def __init__(self, item):
        glImmediateV = item.glinfo.glImmediateFor(item)
        self.render = self.partial(glImmediateV, item.ctypes.data_as(glImmediateV.api.argtypes[-1]))

    def render(self):
        raise NotImplementedError('Replaced at runtime')
MeshLoaderMixin._addLoader_(Immediate, 'immediate')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GLArrayMeshUnit(MatuiMeshUnit):
    def _bindArray(self, arr):
        ainfo = arr.glinfo
        glEnableArray = self.partial(ainfo.glEnableArray, ainfo.glKindId)

        arrPtr = ainfo.glArrayPointer
        #arrPtrType = arrPtr.api.argtypes[-1]
        glArrayPointer = self.partial(arrPtr, arr.shape[-1], arr.glTypeId, 
                arr.strides[-1]*arr.shape[-1], arr.ctypes)#.data_as(arrPtrType))
        return glEnableArray, glArrayPointer

class BoxMesh(GLArrayMeshUnit):
    vertexScale = glData.VertexArray([[0., 0.], [1., 0.], [1., 1.], [0., 1.]], '2f')
    vertex = None

    def __init__(self, box=None):
        if box is not None:
            self.update(box)
    def update(self, box):
        vertex = self.vertex
        if vertex is None:
            vertex = self.vertexScale.copy()
            self.vertex = vertex

        vertex[:] = box.pos + box.size*self.vertexScale
        self.vertexEnable, self.vertexPtr = self._bindArray(vertex)
        count = vertex.size/vertex.shape[-1]
        assert count == 4, count

    def bind(self, actor, res, mgr):
        gl = mgr.gl
        self.drawArray = self.partial(gl.glDrawArrays, gl.GL_QUADS, 0, count)

    def render(self):
        self.vertexEnable()
        self.vertexPtr()
        self.drawArray()
MeshLoaderMixin._addLoader_(BoxMesh, 'boxMesh')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ImageTextureCoordMesh(GLArrayMeshUnit):
    def update(self, imageTexture=None):
        if imageTexture is None:
            return

        self.texCoords = imageTexture.texCoordsForImage()
        self.texCoordsEnable, self.texCoordsPtr = self._bindArray(self.texCoords)

    def render(self):
        self.texCoordsEnable()
        self.texCoordsPtr()
MeshLoaderMixin._addLoader_(ImageTextureCoordMesh, 'imageTextureCoordMesh')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ TextMesh
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TextMesh(MatuiMeshUnit):
    geometry = None
    def update(self, geometry):
        self.geometry = geometry

    def bind(self, actor, res, mgr):
        gl = mgr.gl

        geometry = self.geometry
        count = geometry.size
        self.interleavedArray = self.partial(gl.glInterleavedArrays, geometry.glTypeId, 0, geometry.ctypes)
        self.drawArray = self.partial(gl.glDrawArrays, gl.GL_QUADS, 0, count)

    def render(self):
        self.interleavedArray()
        self.drawArray()

    def interleavedArray(self): pass
    def drawArray(self): pass
MeshLoaderMixin._addLoader_(TextMesh, 'textMesh')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BufferedTextMesh(MatuiMeshUnit):
    geometry = None
    buffer = None
    def update(self, geometry):
        self.geometry = geometry

    def bind(self, actor, res, mgr):
        gl = mgr.gl
        # push the data to the card
        buff = self.buffer 
        if buff is None:
            buff = ArrayBuffer('dynamicDraw')
            self.buffer = buff

        buff.bind()
        buff.sendData(geometry)
        buff.unbind()

        count = geometry.size
        self.interleavedArray = self.partial(gl.glInterleavedArrays, geometry.glTypeId, 0, 0)
        self.drawArray = self.partial(gl.glDrawArrays, gl.GL_QUADS, 0, count)

    def render(self):
        buff = self.buffer
        buff.bind()

        self.interleavedArray()
        self.drawArray()

        buff.unbind()

    def interleavedArray(self): pass
    def drawArray(self): pass
MeshLoaderMixin._addLoader_(BufferedTextMesh, 'bufferedTextMesh')

