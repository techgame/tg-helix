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

from TG.openGL.raw import gl

from .uiBaseViews import UIView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIViewportView(UIView):
    viewForKeys = ['UIViewport'] 

    def init(self, viewport):
        self.viewport = viewport

    def resize(self, size):
        self.viewport.onViewResize(size)
        self.renderViewport()
        self.renderProjection()

    def render(self):
        self.renderProjection()

    def renderPick(self, selector):
        selector.renderProjection(self.viewport.box)
        self.renderProjection(False)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def renderViewport(self):
        box = self.viewport.box
        x, y = box.pos[:2]
        w, h = box.size[:2]

        gl.glViewport(x, y, w, h)

    def renderProjection(self, replaceProjection=True):
        if replaceProjection:
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            gl.glMatrixMode(gl.GL_MODELVIEW)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIOrthoViewportView(UIViewportView):
    viewForKeys = ['UIOrthoViewport'] 

    def renderProjection(self, replaceProjection=True):
        box = self.viewport.box
        x, y, z = box.pos[:3]
        w, h, d = box.size[:3]
        if z == d == 0:
            z = -10
            d =  20

        gl.glMatrixMode(gl.GL_PROJECTION)
        if replaceProjection:
            gl.glLoadIdentity()
        gl.glOrtho(x, x+w, y, y+h, z, z+d)
        gl.glMatrixMode(gl.GL_MODELVIEW)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIBlendViews(UIView):
    viewForKeys = ['UIBlend'] 

    blendModes = {
        'none': (gl.GL_ONE, gl.GL_ZERO),
        'blend': (gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA),
        'multiply': (gl.GL_DST_COLOR, gl.GL_ONE_MINUS_SRC_ALPHA),
        'screen': NotImplemented,
        }

    blendFunc = blendModes['blend']

    def init(self, uiBlend):
        self.blendFunc = self.blendModes[uiBlend.mode]
        gl.glEnable(gl.GL_BLEND)

    def render(self):
        gl.glBlendFunc(*self.blendFunc)

