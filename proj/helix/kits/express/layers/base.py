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
from TG.geomath.data.color import Color

from ..stage import ExpressGraphOp, ExpressActor, ExpressResources
from .. import mesh

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LayerRenderOp(ExpressGraphOp):
    def __init__(self, actor):
        self.res = actor.resData

    def bindPass(self, node, sgo):
        self.res.load(node, sgo)
        return [self.render], None

    def render(self, sgo):
        res = self.res
        res.color()
        res.vertex()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LayerResources(ExpressResources):
    def __init__(self, actor):
        ExpressResources.__init__(self, actor)

        #self.mcolor = mesh.ColorSingle(actor.color)
        self.mcolor = actor.color
        self.mvertex = mesh.BoxMesh(actor.box)
        self.vertex = self.mvertex.render

    def load(self, node, sgo):
        glImmediateV = self.mcolor.glinfo.glImmediateFor(self.mcolor)
        self.color = self._partial(glImmediateV, self.mcolor.ctypes.data_as(glImmediateV.api.argtypes[-1]))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Layer(ExpressActor):
    """
    Layer common features:
        May be a member of many different LayerSets

        Color including Alpha
            Animation
            Add/subtract

        Box
            Animation
            Fit, proportion, etc.

        Transform
            Stack
            Animation
            Translate, Scale, Rotate
    """

    sceneGraphOps = dict(render=LayerRenderOp)
    resData = LayerResources.property()

    box = KVBox.property([[-1, -1], [1, 1]])
    color = Color.property('#FF:FF')

    def isLayer(self): return True
    def isComposite(self): return False

    def __init__(self, color=None):
        ExpressActor.__init__(self)
        if color is not None:
            self.color = color

