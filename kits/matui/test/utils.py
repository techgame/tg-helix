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

from TG.ext.openGL.raw import gl
from TG.ext.openGL.data.arrayViews import arrayView
from TG.ext.openGL.data.drawArrayViews import DrawElementArrayView
from TG.ext.openGL.data.texture import Texture

from TG.helix.kits.matui.theater import MatuiTheater
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
        self.node.maskPass('load')
        if self.res is not None:
            return

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
    _sgOps_ = ['load', 'render']

    box = KVBox.property([0,0], [0,0], dtype='l')
    def __init__(self):
        self._sgGetNode_()

    textBlock = None
    def update(self, typeset):
        self.typeset = typeset
        self.textBlock = typeset.block
        self.textBlock.box = self.box
        self.textBlock.update(typeset)

        self._meshesDirty = True
    _meshesDirty = False

    @property
    def lines(self):
        return self.textBlock.lines

    typeset = None
    @kvobserve('box.*')
    def onBoxUpdate(self, box):
        if self.typeset is None: return
        self.typeset.setWrapSize(box.size, True)
        self.textBlock.update(self.typeset)

    res = None
    def sg_load(self, srm):
        self.node.maskPass('load')
        if self.res is not None:
            return

        res = {}
        res['avColor'] = arrayView('color')
        res['avTexture'] = arrayView('texture_coord')
        res['avVertex'] = arrayView('vertex')
        self.res = res

    def _bindMeshes(self):
        res = self.res
        if res is None:
            return res

        meshes = self.textBlock.meshes
        res['avColor'].bind(meshes['color'])
        res['avTexture'].bind(meshes['texCoords'])
        res['avVertex'].bind(meshes['vertex'])
        res['draw'] = self._bindPages(meshes['pageIdxMap'])

        return res

    _arng4 = numpy.arange(4, dtype='H')
    def _bindPages(self, pageIdxMap):
        texPages = []
        pageTexture = self.pageTexture

        arng4 = self._arng4
        addOuter = numpy.add.outer
        for page, pim in pageIdxMap.items():
            if page is not None:
                av = DrawElementArrayView()
                av.bind('quads', pim)
                texPages.append((av, pageTexture(page)))
        return texPages

    def sg_render(self, srm):
        res = self.res
        if res is None: return

        if self._meshesDirty:
            self._bindMeshes()
            self._meshesDirty = False

        self.textBlock.apply()

        res['avColor'].enable()
        res['avColor'].send()
        res['avTexture'].enable()
        res['avTexture'].send()
        res['avVertex'].enable()
        res['avVertex'].send()

        tex = None
        for av, tex in res['draw']:
            tex.select()
            av.send()
        if tex is not None:
            tex.deselect()

        res['avColor'].disable()
        res['avTexture'].disable()
        res['avVertex'].disable()

    def pageTexture(self, page=None):
        if page is None:
            return None

        tex = getattr(page, 'texture', None)
        if tex is None:
            tex = Texture()
            page.texture = tex
            tex.page = page
            tex.entryCount = None

            tex.texParams += [
                ('target', 'rect'), ('format', 'a'), 
                #('genMipmaps', True),
                ('wrap', gl.GL_CLAMP),
                ##('magFilter', gl.GL_NEAREST), ('minFilter', gl.GL_NEAREST),
                ('magFilter', gl.GL_LINEAR), ('minFilter', gl.GL_LINEAR),
                ]
    
        if page.entryCount > tex.entryCount:
            tex.select()
            size = tex.asValidSize(page.size)
            data = tex.data2d(size=size, format=gl.GL_ALPHA, dataType=gl.GL_UNSIGNED_BYTE)
            data.texArray(page.data, dict(alignment=1,))

            if any(page.size != tex.texSize):
                data.setImageOn(tex)
            else: data.setSubImageOn(tex)
            tex.deselect()
            tex.entryCount = page.entryCount

        return tex

