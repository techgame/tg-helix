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

from TG.openGL.raw.gl import *

from .uiViewBase import UIView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewportView(UIView):
    viewForKeys = ['Viewport'] 

    def init(self, viewport):
        self.viewport = viewport

    def resize(self, size):
        self.viewport.onViewResize(size)

        box = self.viewport.box
        x, y = box.pos[:2]
        w, h = box.size[:2]

        glViewport(x, y, w, h)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def render(self):
        glLoadIdentity()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class OrthoViewportView(ViewportView):
    viewForKeys = ['OrthoViewport'] 

    def resize(self, size):
        self.viewport.onViewResize(size)

        box = self.viewport.box
        x, y, z = box.pos[:3]
        w, h, d = box.size[:3]
        if z == d == 0:
            z = -10
            d =  20

        glViewport(x, y, w, h)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(x, x+w, y, y+h, z, z+d)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

