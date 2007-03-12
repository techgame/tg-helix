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
from TG.openGL.data import Rect, Vector, Color
from TG.openGL.raw import gl

from .stage import ExpressActor
from . import mesh

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LayerRenderOp(object):
    cullStack = False
    def __init__(self, actor):
        self.actor = actor
    def bind(self, node, mgr):
        return [self.render]
    def bindUnwind(self, node, mgr):
        return []

    def render(self):
        actor = self.actor
        actor.geomColor()
        actor.geomRender()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Layer(ExpressActor):
    """
    Layer common features:
        May be a member of many different LayerSets

        Color including Alpha
            Animation
            Add/subtract

        Rectangle Geometry
            Animation
            Fit, proportion, etc.

        Transform
            Stack
            Animation
            Translate, Scale, Rotate
    """

    sceneGraphOps = dict(
        render=LayerRenderOp,
        resize=None)
    box = Rect.property()
    color = Color.property('#00:FF')

    def isLayer(self): return True
    def isComposite(self): return False

    def __init__(self, color=None, box=None):
        ExpressActor.__init__(self)
        if color is not None:
            self.color = color
        if box is not None:
            self.box = box

        self._configResources()

    def _configResources(self):
        self.geom = mesh.BoxMesh(self.box)
        self.geomRender = self.geom.render

        glImmediateV = self.color.glinfo.glImmediateFor(self.color)
        self.geomColor = partial(glImmediateV, self.color.ctypes.data_as(glImmediateV.api.argtypes[-1]))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Background Layer
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BGLayerRenderOp(LayerRenderOp):
    def render(self):
        actor = self.actor
        box = actor.box
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(box.left, box.right, box.bottom, box.top, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)

        actor.geomColor()
        actor.geomRender()

class BGLayerResizeOp(object):
    cullStack = False
    def __init__(self, actor):
        self.actor = actor
    def bind(self, node, mgr):
        return [partial(self.resize, mgr)]
    def bindUnwind(self, node, mgr):
        return []

    def resize(self, mgr):
        actor = self.actor
        actor.box.size[:] = mgr.viewportSize
        actor.geom.update(actor.box)

        gl.glViewport(0,0,*mgr.viewportSize)

class BackgroundLayer(Layer):
    sceneGraphOps = dict(
        render=BGLayerRenderOp,
        resize=BGLayerResizeOp)

    box = Rect.property()

