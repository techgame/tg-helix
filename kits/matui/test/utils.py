#!/usr/bin/env python
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

import numpy

from TG.kvObserving import KVProperty, kvobserve

from TG.geomath.data.kvBox import KVBox
from TG.geomath.data.color import Color

from TG.openGL.raw import gl
from TG.openGL.data.arrayViews import arrayView
from TG.openGL.data.texture import Texture

from TG.helix.bridges.wx.host import HelixHost
from TG.helix.kits.matui.scene import MatuiScene
from TG.helix.kits.matui.actor import MatuiActor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Viewport(MatuiActor):
    _sgOps_ = [('resize', 'adjust'), ('render', 'adjust')]
    box = KVBox.property([0,0], [1,1], dtype='i')
    mask = gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT

    def adjust(self, srm):
        box = self.box
        box.p1 = srm.vpsize
        gl.glViewport(*box.toflatlist())
        gl.glClear(self.mask)

class ScreenOrtho(MatuiActor):
    _sgOps_ = ['load', 'resize', 'render']
    box = KVBox.property([0,0,-1], [1,1,1], dtype='i')

    def __init__(self):
        self._sgGetNode_()

    def sg_load(self, srm):
        self.box[1,:2] = srm.vpsize
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def sg_resize(self, srm):
        self.box[1,:2] = srm.vpsize

    def sg_render(self, srm):
        ((x0, y0, z0),
         (x1, y1, z1)) = self.box.pv

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(x0, x1, y0, y1, z0, z1)
        gl.glMatrixMode(gl.GL_MODELVIEW)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Panel(MatuiActor):
    _sgOps_ = [ 'load', 'render']

    color = Color.property(['#ff', '#ff', '#00', '#00'])
    box = KVBox.property([-1,-1], [1,1], dtype='f')

    def __init__(self):
        self._sgGetNode_()

    res = None
    def sg_load(self, srm):
        if self.res is not None:
            return
        self.sgClearOp('load')

        res = {}
        self.res = res

        avColor = arrayView('color')
        res['avColor'] = avColor
        avColor.bind(self.color)

        boxMesh = self.box.geoXfrm('quads')
        res['boxMesh'] = boxMesh
        self.onBoxUpdate(self.box)

        avVertex = arrayView('vertex')
        res['avVertex'] = avVertex
        avVertex.bind(boxMesh)

        avDraw = arrayView('draw_array')
        avDraw.bind('quads', boxMesh.size/boxMesh.shape[-1])
        res['avDraw'] = avDraw

    @kvobserve('box.*')
    def onBoxUpdate(self, box):
        res = self.res
        if res is None: return
        boxMesh = self.res['boxMesh']
        boxMesh[:] = box.geoXfrm('quads')

    def sg_render(self, srm):
        res = self.res
        res['avColor'].enable()
        res['avColor'].send()
        res['avVertex'].enable()
        res['avVertex'].send()
        res['avDraw'].send()
        res['avColor'].disable()
        res['avVertex'].disable()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Text(MatuiActor):
    _sgOps_ = [ 'load', 'render' ]

    box = KVBox.property([0,0], [0,0], dtype='l')

    def __init__(self):
        self._sgGetNode_()

    _sorts = None
    def getSorts(self):
        return self._sorts
    def setSorts(self, sorts):
        self._sorts = sorts

        if sorts is None: count = 1
        else: count = len(sorts)
        self.mesh = numpy.zeros((count, 4, 2), 'l')
        self.texMesh = numpy.zeros((count, 4, 2), 'f')
        self.colorMesh = numpy.zeros((count, 4, 4), 'B')

        if sorts is not None:
            offset = sorts['offset']
            self.colorMesh[:] = sorts['color']
            self.page = self.arena.texCoords(sorts, self.texMesh)
            self.box.size = offset[-1]-offset[0]
        else:
            self.page = None
            self.box.size = 0

        if self.res is not None:
            self.rebind()
    sorts = property(None, setSorts)

    @kvobserve('box.*')
    def onBoxUpdate(self, box):
        res = self.res
        if res is None: return

        sorts = self.getSorts()
        if sorts is None: return

        t0 = self.box.p0
        self.mesh[:] = t0
        self.mesh[:] += sorts['quad']
        self.mesh[:] += sorts['offset']

    res = None
    def sg_load(self, srm):
        if self.res is not None:
            return
        self.sgClearOp('load')

        res = {}
        res['avColor'] = arrayView('color')
        res['avTexCoords'] = arrayView('texture_coord')
        res['avVertex'] = arrayView('vertex')
        res['avDraw'] = arrayView('draw_array')

        tex = Texture()
        tex.texParams += [
            ('target', 'rect'), 
            ('format', 'a'), 
            ('wrap', gl.GL_CLAMP),
            # Nearest provides EXACT font rendering, without aliasing.  However it does not scale as well.
            ('magFilter', gl.GL_NEAREST), ('minFilter', gl.GL_NEAREST),

            # Linear provides nearly exact font rendering.  It scales better than nearest.
            #('magFilter', gl.GL_LINEAR), ('minFilter', gl.GL_LINEAR),
            ]
        res['texture'] = tex

        self.res = res
        self.rebind()
    page = None

    def rebind(self):
        res = self.res
        res['avColor'].bind(self.colorMesh)
        res['avTexCoords'].bind(self.texMesh)

        mesh = self.mesh
        res['avVertex'].bind(mesh)
        res['avDraw'].bind('quads', mesh.size/mesh.shape[-1])

        page = self.page
        if page is not None:
            tex = res['texture']
            tex.select()
            size = tex.asValidSize(page.size)
            data = tex.data2d(size=size, format=gl.GL_ALPHA, dataType=gl.GL_UNSIGNED_BYTE)
            data.texArray(page.data, dict(alignment=1,))

            if any(page.size != tex.texSize):
                data.setImageOn(tex)
            else: data.setSubImageOn(tex)
            tex.deselect()

    def sg_render(self, srm):
        res = self.res
        res['texture'].select()

        res['avColor'].enable()
        res['avColor'].send()
        res['avTexCoords'].enable()
        res['avTexCoords'].send()
        res['avVertex'].enable()
        res['avVertex'].send()

        res['avDraw'].send()

        res['avColor'].disable()
        res['avTexCoords'].disable()
        res['avVertex'].disable()

        res['texture'].deselect()

