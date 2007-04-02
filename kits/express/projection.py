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

from TG.geomath.data.kvBox import KVBox

from TG.openGL.raw import gl

from .stage import ExpressGraphOp, ExpressActor, ExpressResources

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Viewport Actor
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewportResizeOp(ExpressGraphOp):
    def __init__(self, actor, sgNode):
        self.viewport = actor.viewport

    def bindPass(self, sgNode, sgo):
        return [self.resize], None

    def resize(self, sgo):
        gl.glViewport(0,0,*sgo.viewportSize)
        self.viewport.p1 = sgo.viewportSize

class Viewport(ExpressActor):
    sceneGraphOps = dict(render=None, resize=ViewportResizeOp)
    viewport = KVBox.property()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Projection Actor
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ProjectionRenderOp(ExpressGraphOp):
    def __init__(self, actor, sgNode):
        self.box = actor.box

    def bindPass(self, sgNode, sgo):
        return [self.render], None

    def render(self, sgo):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        (x0, y0, z0, 
         x1, y1, z1) = self.box.pv.flat
        gl.glOrtho(x0, x1, y0, y1, z0, z1)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ProjectionResizeOp(ExpressGraphOp):
    def __init__(self, actor, sgNode):
        self.boxBase = actor.boxBase
        self.box = actor.box

    def bindPass(self, sgNode, sgo):
        return [self.resize], None

    def resize(self, sgo):
        aspect = dict(size=sgo.viewportSize, grow=True)
        self.box[:] = self.boxBase.atAspect[aspect, 0.5]

class Projection(ExpressActor):
    sceneGraphOps = dict(
        render=ProjectionRenderOp,
        resize=ProjectionResizeOp)

    boxBase = KVBox.property([-100, -100, -100], [100, 100, 100])
    box = KVBox.property([-1, -1, -1], [1, 1, 1])

