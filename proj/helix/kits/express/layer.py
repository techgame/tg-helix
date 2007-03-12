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

from .stage import ExpressGraphOp, ExpressActor
from . import mesh

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LayerRenderOp(ExpressGraphOp):
    def bind(self, node, mgr):
        self.actor.configResources()
        return [self.render]
    def render(self):
        actor = self.actor
        actor.geomColor()
        actor.geom.render()

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

    geom = None
    def configResources(self):
        if self.geom is None:
            self._configResources()
        return True

    def _configResources(self):
        self.geom = mesh.BoxMesh(self.box)

        glImmediateV = self.color.glinfo.glImmediateFor(self.color)
        self.geomColor = partial(glImmediateV, self.color.ctypes.data_as(glImmediateV.api.argtypes[-1]))

