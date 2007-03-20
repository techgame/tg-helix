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

from TG.openGL.raw import gl
from TG.geomath.data.color import Color

from ..stage import ExpressGraphOp
from .base import Layer, LayerRenderOp

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Background Layer
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BGLayerRenderOp(LayerRenderOp):
    def __init__(self, actor):
        self.res = actor.resData
        self.actorBox = actor.box
    def render(self):
        box = self.actorBox

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        l,b,r,t = box.pv.flat
        gl.glOrtho(l, r, b, t, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)

        LayerRenderOp.render(self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BGLayerResizeOp(ExpressGraphOp):
    def __init__(self, actor):
        self.actorBox = actor.box

    def bind(self, node, mgr):
        return [self._partial(self.resize, mgr)]
    def resize(self, mgr):
        gl.glViewport(0,0,*mgr.viewportSize)

        self.actorBox.setAspectWithSize(
                        (mgr.viewportAspect, True), 
                        size=(2, 2), at=0.5)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Background layer
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BackgroundLayer(Layer):
    sceneGraphOps = dict(
        render=BGLayerRenderOp,
        resize=BGLayerResizeOp)

    color = Color.property('#00:ff')
