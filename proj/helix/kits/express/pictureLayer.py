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
from TG.openGL.data.image import ImageTextureRect, ImageTexture2d

from .stage import ExpressGraphOp
from .layer import Layer
from . import mesh

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PictureLayerRenderOp(ExpressGraphOp):
    def bind(self, node, mgr):
        self.actor.configResources()
        return [self.render]
    def render(self):
        actor = self.actor
        actor.geomColor()
        actor.texture.select()
        actor.geomTexCoords.render()
        actor.geom.render()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PictureLayer(Layer):
    """Displays geometry with a texture"""

    sceneGraphOps = dict(render=PictureLayerRenderOp)

    def __init__(self, image=None, color=None, box=None):
        if image is not None:
            self.load(image)
        Layer.__init__(self, color, box)

    image = None
    openImage = staticmethod(PIL.Image.open)
    def load(self, image, size=None):
        if isinstance(image, basestring):
            image = self.openImage(image)
        if size is not None:
            image = image.resize(size)
        self.image = image
        imageAspect = image.size[0]/float(image.size[1])
        self.box.setSize((2,2), imageAspect)
        self.box.pos[:] = -.5*self.box.size
        return image

    def _configResources(self):
        Layer._configResources(self)

        #texture = ImageTexture2d(self.image)
        texture = ImageTextureRect(self.image)
        texture.deselect()
        self.texture = texture
        self.geomTexCoords = mesh.ImageTextureCoordMesh(texture)

