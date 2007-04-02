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

from TG.kvObserving import KVProperty
from TG.quicktime import quickTimeMovie
from TG.geomath.data.kvBox import KVBox

from .base import Layer, LayerRenderOp, LayerResources
from .. import mesh

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class QTTextureLayerRenderOp(LayerRenderOp):
    def render(self, sgo):
        res = self.res

        res.qtTextureUpdate()

        res.texture()
        res.color()
        res.texcoords()
        res.vertex()
        res.notexture()

        res.qtMediaProcess()

class QTTextureLayerResources(LayerResources):
    def __init__(self, actor):
        qtMedia = actor.qtMedia
        qtMedia.process(0.05)
        qtTexture = qtMedia.qtTexture
        qtTexture.update(True)

        actor.aspect = qtTexture.size[0]/float(qtTexture.size[1])

        LayerResources.__init__(self, actor)

        self.mtexture = qtTexture
        self.qtTextureUpdate = qtTexture.update
        self.mtexture.deselect()
        self.texture = self.mtexture.select
        self.notexture = self.mtexture.deselect

        self.qtMediaProcess = qtMedia.process

        self.mtexcoords = mesh.QTTextureCoordMesh(self.mtexture.texCoords)
        self.texcoords = self.mtexcoords.render


class QTLayer(Layer):
    """Displays geometry with a quicktime texture
    
    Picture layer
        Preload
        Contrast, brightness, saturation
            Implement with shader?
    """

    sceneGraphOps = dict(render=QTTextureLayerRenderOp)
    resData = QTTextureLayerResources.property()

    qtMedia = KVProperty(None)

    hostBox = KVBox.property([[-100, -100], [100, 100]])
    aspect = KVProperty(1)
    
    def __init__(self, path=None, color=None, hostBox=None):
        self.kvwatch('hostBox.*')(self._updateBoxAspect)
        self.kvwatch('aspect')(self._updateBoxAspect)

        Layer.__init__(self, color)
        self.qtMedia = quickTimeMovie.QTMovie()
        if path is not None:
            self.loadPath(path)
        if hostBox is not None:
            self.hostBox = hostBox

    def loadPath(self, path):
        self.qtMedia.loadPath(path)

    def _updateBoxAspect(self, kvw, key):
        self.box.atAspect[self.aspect, .5] = self.hostBox.size

class QTMovieLayer(QTLayer):
    """Displays geometry with a quicktime movie texture

    Movie layer
        Preload
        Loop / Palindrome
        Direction - Forward/Backward
        Play speed
        Seeking
            Forward/backward/time?
        Volume
            What about redirecting output?
    """

    def play(self): self.qtMedia.start()
    def pause(self): self.qtMedia.pause()
    def stop(self): self.qtMedia.stop()

    def looping(self, bloop=True): self.qtMedia.setLooping(bloop)
    def palindrome(self, bloop=True): self.qtMedia.setLooping(bloop and 2 or 0)

