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

from .stage import ExpressGraphOp
from .layer import Layer

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Background Layer
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BGLayerRenderOp(ExpressGraphOp):
    def bind(self, node, mgr):
        self.actor.configResources()
        return [self.render]
    def render(self):
        actor = self.actor
        box = actor.box
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(box.left, box.right, box.bottom, box.top, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)

        actor.geomColor()
        actor.geom.render()

class BGLayerResizeOp(ExpressGraphOp):
    def bind(self, node, mgr):
        self.actor.configResources()
        return [self._partial(self.resize, mgr)]
    def resize(self, mgr):
        actor = self.actor
        actor.box.size[:] = mgr.viewportSize
        actor.geom.update(actor.box)

        gl.glViewport(0,0,*mgr.viewportSize)

class BackgroundLayer(Layer):
    sceneGraphOps = dict(
        render=BGLayerRenderOp,
        resize=BGLayerResizeOp)

