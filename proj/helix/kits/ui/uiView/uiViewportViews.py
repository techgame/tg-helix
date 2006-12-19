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

from .uiViewBase import UIView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIViewportView(UIView):
    viewForKeys = ['UIViewport'] 

    def init(self, viewport):
        self.viewport = viewport

    def resize(self, size):
        self.viewport.onViewResize(size)

        box = self.viewport.box
        x, y = box.pos[:2]
        w, h = box.size[:2]

        gl.glViewport(x, y, w, h)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    def render(self):
        gl.glLoadIdentity()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIOrthoViewportView(UIViewportView):
    viewForKeys = ['UIOrthoViewport'] 

    def resize(self, size):
        self.viewport.onViewResize(size)

        box = self.viewport.box
        x, y, z = box.pos[:3]
        w, h, d = box.size[:3]
        if z == d == 0:
            z = -10
            d =  20

        gl.glViewport(x, y, w, h)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(x, x+w, y, y+h, z, z+d)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIBlendViews(UIView):
    viewForKeys = ['UIBlend'] 

    blendModes = {
        'none': (gl.GL_ONE, gl.GL_ZERO),
        'blend': (gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA),
        'multiply': (gl.GL_DST_COLOR, gl.GL_ONE_MINUS_SRC_ALPHA),
        }

    blendFunc = blendModes['blend']

    def init(self, uiBlend):
        self.blendFunc = self.blendModes[uiBlend.mode]
        gl.glEnable(gl.GL_BLEND)

    def render(self):
        gl.glBlendFunc(*self.blendFunc)

