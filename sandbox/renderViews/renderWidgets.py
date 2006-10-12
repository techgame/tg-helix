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

from TG.openGL.raw import gl, glu, glext
from TG.openGL.raw.gl import *

from TG.helixui.actors.basic import HelixActor, Widget, ViewportBounds

from renderViews import RenderView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewportBoundsView(RenderView):
    viewForKeys = [ViewportBounds] 

    def resize(self, actor, size):
        actor.setViewportSize(size)
    def render(self, actor):
        glViewport(*actor.xywh())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ClearBuffers(HelixActor):
    color = (0.01, 0.01, 0.01, 0.0)
    depth = 1.0

class ClearBuffersView(RenderView):
    viewForKeys = [ClearBuffers]

    def renderInitial(self, actor):
        glClearColor(*actor.color)
        glClearDepth(actor.depth)

    def render(self, actor):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

