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

from functools import partial

import numpy

from TG.openGL import data as glData
from TG.openGL.raw import gl
from TG.openGL.data.bufferObjects import ArrayBuffer

from TG.openGL.data.image import ImageTextureRect, ImageTexture2d

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GLArrayMesh(object):
    partial = staticmethod(partial)
    def _bindArray(self, arr):
        ainfo = arr.glinfo
        glEnableArray = self.partial(ainfo.glEnableArray, ainfo.glKindId)

        arrPtr = ainfo.glArrayPointer
        #arrPtrType = arrPtr.api.argtypes[-1]
        glArrayPointer = self.partial(arrPtr, arr.shape[-1], arr.glTypeId, 
                arr.strides[-1]*arr.shape[-1], arr.ctypes)#.data_as(arrPtrType))
        return glEnableArray, glArrayPointer

    mesh = glData.VertexArray([], '2f')
    def bindMesh(self):
        self.aoEnable, self.aoBindPtr = self._bindArray(self.mesh)

    def render(self):
        self.aoEnable()
        self.aoBindPtr()

class GLVertexMesh(GLArrayMesh):
    def bindDraw(self):
        mesh = self.mesh
        count = mesh.size/mesh.shape[-1]
        self.drawArray = self.partial(gl.glDrawArrays, gl.GL_QUADS, 0, count)

class BoxMesh(GLVertexMesh):
    mesh = glData.VertexArray([[0., 0.], [1., 0.], [1., 1.], [0., 1.]], '2f')

    def __init__(self, box=None):
        self.mesh = self.mesh.copy()
        self.bindMesh()
        self.bindDraw()

        box.kvpub.add('*', self.updateMesh)
        self.updateMesh(box, '*')

    def updateMesh(self, box, key):
        self.mesh[:] = box.geoXfrm('quads')

    def render(self):
        self.aoEnable()
        self.aoBindPtr()
        self.drawArray()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class QTTextureCoordMesh(GLArrayMesh):
    def __init__(self, texCoords=None):
        self.mesh = glData.TexCoordArray(texCoords)
        self.bindMesh()

class ImageTextureCoordMesh(GLArrayMesh):
    def __init__(self, imageTexture=None):
        if imageTexture is not None:
            self.update(imageTexture)
    def update(self, imageTexture=None):
        if imageTexture is None:
            return

        self.mesh = imageTexture.texCoordsForImage()
        self.bindMesh()

    def render(self):
        self.tcaEnable()
        self.tcaBindPtr()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ TextMesh
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TextMesh(object):
    partial = staticmethod(partial)

    geometry = None
    def update(self, geometry):
        self.geometry = geometry

        count = geometry.size
        if count > 0:
            self.interleavedArray = self.partial(gl.glInterleavedArrays, geometry.glTypeId, 0, geometry.ctypes)
            self.drawArray = self.partial(gl.glDrawArrays, gl.GL_QUADS, 0, count)
        else:
            self.interleavedArray = lambda: None
            self.drawArray = lambda: None

    def render(self):
        self.interleavedArray()
        self.drawArray()

    def interleavedArray(self): pass
    def drawArray(self): pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BufferedTextMesh(object):
    geometry = None
    buffer = None
    def update(self, geometry):
        self.geometry = geometry

        # push the data to the card
        buff = self.buffer 
        if buff is None:
            buff = ArrayBuffer('dynamicDraw')
            self.buffer = buff

        buff.bind()
        buff.sendData(geometry)
        buff.unbind()

        count = geometry.size
        if count > 0:
            self.interleavedArray = self.partial(gl.glInterleavedArrays, geometry.glTypeId, 0, 0)
            self.drawArray = self.partial(gl.glDrawArrays, gl.GL_QUADS, 0, count)
        else:
            self.interleavedArray = lambda: None
            self.drawArray = lambda: None

    def render(self):
        buff = self.buffer
        buff.bind()

        self.interleavedArray()
        self.drawArray()

        buff.unbind()

    def interleavedArray(self): pass
    def drawArray(self): pass

