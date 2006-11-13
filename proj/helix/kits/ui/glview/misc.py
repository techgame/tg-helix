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

from TG.helix.framework.actors import HelixActor

from .scene import UIView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ClearBuffers(HelixActor):
    color = (0.0, 0.0, 0.0, 0.0)
    depth = 1.0
    mask = GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT

    def __init__(self, color=None, depth=None):
        if color is not None:
            self.color = color
        if depth is not None:
            self.depth = depth

class ClearBuffersView(UIView):
    viewForKeys = [ClearBuffers]

    def render(self):
        viewable = self.viewable
        glClearColor(*viewable.color)
        glClearDepth(viewable.depth)
        glClear(viewable.mask)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewportBoundsView(UIView):
    viewForKeys = ['ViewportBounds'] 

    def resize(self, size):
        self.viewable.setViewportSize(size)
    def render(self):
        glViewport(*self.viewable.xywh())

