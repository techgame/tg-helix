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

from .layer import Layer, LayerRenderOp, LayerResources
from . import mesh

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TextureLayerRenderOp(LayerRenderOp):
    def render(self):
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

    def __init__(self, image=None, color=None):
        if image is not None:
            self.load(image)
        Layer.__init__(self, color)

    openImage = staticmethod(PIL.Image.open)
    def load(self, image, size=None):
        if isinstance(image, basestring):
            image = self.openImage(image)
        if size is not None:
            image = image.resize(size)
        self.image = image
        self.box.setAspect(image.size, at=.5)
        return image

