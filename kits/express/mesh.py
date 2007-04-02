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

from TG.openGL.raw import gl
from TG.openGL.data.bufferObjects import ArrayBuffer
from TG.openGL.data.arrayViews import arrayView

from TG.openGL.data.image import ImageTextureRect, ImageTexture2d

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GLArrayMesh(object):
    meshKind = 'vertex'
    meshView = None
    mesh = None
    def bindMesh(self):
        meshView = self.meshView
        if meshView is None:
            meshView = arrayView(self.meshKind)
            self.meshView = meshView
        meshView.bind(self.mesh)

    def render(self):
        meshView = self.meshView
        meshView.enable()
        meshView.send()

class GLVertexMesh(GLArrayMesh):
    meshDraw = None
    def bindDraw(self):
        meshDraw = self.meshDraw
        if meshDraw is None:
            meshDraw = arrayView('draw_array')
            self.meshDraw = meshDraw

        mesh = self.mesh
        meshDraw.bind('quads', mesh.size/mesh.shape[-1])

class BoxMesh(GLVertexMesh):
    mesh = numpy.array([[0., 0.], [1., 0.], [1., 1.], [0., 1.]], 'f')

    def __init__(self, box=None):
        self.mesh = self.mesh.copy()
        self.bindMesh()
        self.bindDraw()

        box.kvpub.add('*', self.updateMesh)
        self.updateMesh(box, '*')

    def updateMesh(self, box, key):
        self.mesh[:] = box.geoXfrm('quads')

    def render(self):
        meshView = self.meshView
        meshView.enable()
        meshView.send()
        self.meshDraw.send()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class QTTextureCoordMesh(GLArrayMesh):
    meshKind = 'texture_coord'
    def __init__(self, texCoords=None):
        self.mesh = numpy.array(texCoords)
        self.bindMesh()

class ImageTextureCoordMesh(GLArrayMesh):
    meshKind = 'texture_coord'
    def __init__(self, imageTexture=None):
        if imageTexture is not None:
            self.update(imageTexture)
    def update(self, imageTexture=None):
        if imageTexture is None:
            return

        self.mesh = imageTexture.texCoordsForImage()
        self.bindMesh()

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
    partial = staticmethod(partial)
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

