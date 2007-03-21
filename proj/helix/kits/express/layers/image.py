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

import PIL.Image

from TG.kvObserving import KVProperty
from TG.geomath.data.kvBox import KVBox

from .base import Layer, LayerRenderOp, LayerResources
from .. import mesh

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TextureLayerRenderOp(LayerRenderOp):
    def render(self, sgo):
        res = self.res
        res.texture()
        res.color()
        res.texcoords()
        res.vertex()
        res.notexture()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TextureLayerResources(LayerResources):
    def __init__(self, actor):
        LayerResources.__init__(self, actor)

        self.mtexture = mesh.ImageTextureRect(actor.image)
        self.mtexture.deselect()
        self.texture = self.mtexture.select
        self.notexture = self.mtexture.deselect

        self.mtexcoords = mesh.ImageTextureCoordMesh(self.mtexture)
        self.texcoords = self.mtexcoords.render

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ImageLayer(Layer):
    """Displays geometry with a texture"""

    sceneGraphOps = dict(render=TextureLayerRenderOp)
    resData = TextureLayerResources.property()

    image = KVProperty(None)

    hostBox = KVBox.property([[-100, -100], [100, 100]])
    aspect = KVProperty(1)

    def __init__(self, image=None, color=None, hostBox=None):
        self.kvwatch('hostBox.*')(self._updateBoxAspect)
        self.kvwatch('aspect')(self._updateBoxAspect)

        if image is not None:
            self.load(image)
        Layer.__init__(self, color)

        if hostBox is not None:
            self.hostBox = hostBox

    openImage = staticmethod(PIL.Image.open)
    def load(self, image, size=None):
        if isinstance(image, basestring):
            image = self.openImage(image)
        if size is not None:
            image = image.resize(size)
        self.image = image
        self.aspect = image.size[0].__truediv__(image.size[1])
        #self.box.setAspect(image.size, at=.5)
        return image

    def _updateBoxAspect(self, kvw, key):
        self.box.atAspect[self.aspect, .5] = self.hostBox.size

