##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from .units import MatuiLoaderMixin, MatuiMaterialUnit

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Loader Mixin
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MaterialLoaderMixin(MatuiLoaderMixin):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Material Resources
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiMaterial(MatuiMaterialUnit):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MultiMaterial(MatuiMaterial):
    def __init__(self, materials=None):
        if materials:
            self.materials = materials

    def __getitem__(self, idx):
        return self.materials.__getitem__(idx)
    def insert(self, idx, material):
        assert material.isResourceMaterial()
        self.materials.insert(idx, material)
    def append(self, material):
        assert material.isResourceMaterial()
        self.materials.append(material)
    __iadd__ = append

    def bind(self, actor, res, mgr):
        result = []
        for mat in self.materials:
            result += mat.bind(actor, res, mgr)
        return result

    def bindUnwind(self, actor, res, mgr):
        result = []
        for mat in reversed(self.materials):
            result += mat.bindUnwind(actor, res, mgr)
        return result
MaterialLoaderMixin._addLoader_(MultiMaterial, 'multiMaterial')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DebugMaterial(MatuiMaterial):
    def __init__(self, name, incResources=False):
        self.name = name
        self.incResources = incResources
    def bind(self, actor, res, mgr):
        if self.incResources:
            return [self.partial(self.dbgResources, actor, res, mgr)]
        else: return [self.partial(self.dbgSimple, actor, res, mgr)]

    def dbgSimple(self, actor, res, mgr):
        print '%s: %r' % (self.name, actor)
    def dbgResources(self, actor, res, mgr):
        print '%s: %r' % (self.name, actor)
        print '  - res: %s' % (', '.join(res.keys()),)
MaterialLoaderMixin._addLoader_(DebugMaterial, 'debugMaterial')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ResizeLayoutMaterial(MatuiMaterial):
    cullStack = False
    def __init__(self, cullStack=False):
        self.cullStack = cullStack

    def bind(self, actor, res, mgr):
        return [self.partial(self.perform, actor, res, mgr)]
    def perform(self, actor, res, mgr):
        res['layout'].layoutInBox(mgr.stage.box)
MaterialLoaderMixin._addLoader_(ResizeLayoutMaterial, 'resizeLayoutMaterial')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PickRenderer(MatuiMaterial):
    def bind(self, actor, res, mgr):
        return [self.partial(mgr.pushItem, actor)]
    def bindUnwind(self, actor, res, mgr):
        return [mgr.popItem]
MaterialLoaderMixin._addLoader_(PickRenderer, 'pickRenderer')

class ActorPickRenderer(MatuiMaterial):
    def bind(self, actor, res, mgr):
        result = res['render'].bind(actor, res, mgr)
        result.insert(0, self.partial(mgr.pushItem, actor))
        return result
    def bindUnwind(self, actor, res, mgr):
        result = res['render'].bindUnwind(actor, res, mgr)
        result.append(mgr.popItem)
        return result
MaterialLoaderMixin._addLoader_(ActorPickRenderer, 'actorPickRenderer')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ GL Materials
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OrthoProjectionMaterial(MatuiMaterial):
    def bind(self, actor, res, mgr):
        return [self.partial(self.render, actor, mgr.gl)]
    def render(self, actor, gl):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        x1, y1 = actor.box.pos
        x2, y2 = actor.box.corner
        gl.glOrtho(x1, x2, y1, y2, -10, 10)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()

    def bindUnwind(self, actor, res, mgr):
        return [self.partial(self.renderUnwind, mgr.gl)]
    def renderUnwind(self, gl):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()
MaterialLoaderMixin._addLoader_(OrthoProjectionMaterial, 'orthoProjectionMaterial')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BlendMaterial(MatuiMaterial):
    def __init__(self, mode='blend'):
        self.mode = mode

    def bind(self, actor, res, mgr):
        gl = mgr.gl
        gl.glEnable(gl.GL_BLEND)

        blendModes = {
            'none': (gl.GL_ONE, gl.GL_ZERO),
            'blend': (gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA),
            'multiply': (gl.GL_DST_COLOR, gl.GL_ONE_MINUS_SRC_ALPHA),
            'screen': NotImplemented,
            }

        return [self.partial(gl.glBlendFunc, blendModes[self.mode])]
MaterialLoaderMixin._addLoader_(BlendMaterial, 'blendMaterial')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatrixMaterial(MatuiMaterial):
    pos = (0,0,0)
    scale = (1,1,1)

    def __init__(self, pos=None, scale=None):
        if pos is not None:
            self.setTranslate(pos)
        if scale is not None:
            self.setScale(scale)

    def setTranslate(self, (x,y,z)):
        self.pos = (x,y,z)
    def setUniformScale(self, s):
        self.setScale((s,s,s))
    def setScale(self, (sx, sy, sz)):
        self.scale = (sx,sy,sz)

    def bind(self, actor, res, mgr):
        return [self.partial(self.render, mgr.gl)]
    def render(self, gl):
        gl.glPushMatrix()
        gl.glTranslatef(*self.pos)
        gl.glScalef(*self.scale)

    def bindUnwind(self, actor, res, mgr):
        return [mgr.gl.glPopMatrix]
MaterialLoaderMixin._addLoader_(MatrixMaterial, 'matrixMaterial')

