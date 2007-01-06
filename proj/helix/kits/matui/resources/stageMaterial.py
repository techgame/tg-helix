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

from TG.openGL.selection import NameSelector
from TG.openGL.raw import gl

from .material import MatuiMaterial, MaterialLoaderMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@MaterialLoaderMixin._addLoader_
def stageMaterialGroup():
    return dict(
            render=StageRenderMaterial(),
            pick=StagePickMaterial(),
            resize=StageResizeMaterial(),)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StageRenderMaterial(MatuiMaterial):
    mask = gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT
    gl = gl

    def bind(self, actor, res, mgr):
        return [self.perform]
    def perform(self):
        gl = self.gl
        gl.glClear(self.mask)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StageResizeMaterial(MatuiMaterial):
    gl = gl

    def bind(self, stage, res, mgr):
        return [self.partial(self.perform, stage, mgr)]
    def perform(self, stage, mgr):
        gl = self.gl
        w, h = mgr.viewportSize
        stage.box.size[:2] = (w, h)
        gl.glViewport(0, 0, w, h)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StagePickMaterial(MatuiMaterial):
    gl = gl

    SelectorFactory = NameSelector
    def __init__(self):
        self.selector = self.SelectorFactory()

    def bind(self, actor, res, mgr):
        return [self.partial(self.perform, actor, res, mgr)]
    def perform(self, stage, res, mgr):
        selector = self.selector
        selector.start()
        mgr.startSelector(selector)

        gl = self.gl
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        selector.pickMatrix(stage.box, mgr.selectPos, mgr.selectSize)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def bindUnwind(self, actor, res, mgr):
        return [self.partial(self.performUnwind, actor, res, mgr)]
    def performUnwind(self, actor, res, mgr):
        selector = self.selector
        selection = selector.finish()
        selection.sort()
        selection = [s[-1] for s in selection]

        mgr.finishSelector(selector, selection)

