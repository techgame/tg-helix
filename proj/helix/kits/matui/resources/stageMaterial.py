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
            #pick=StageDebugPickMaterial(),
            resize=StageResizeMaterial(),)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StageRenderMaterial(MatuiMaterial):
    mask = gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT
    gl = gl

    def bind(self, stage, res, mgr):
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

    def bind(self, stage, res, mgr):
        return [self.partial(self.perform, stage, mgr)]
    def perform(self, stage, mgr):
        gl = self.gl
        selector = self.selector
        selector.start()

        mgr.startSelector(selector)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        vpbox = stage.box.astype(int).tolist()
        selector.pickMatrix(mgr.selectPos, mgr.selectSize, vpbox)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def bindUnwind(self, stage, res, mgr):
        return [self.partial(self.performUnwind, stage, mgr)]
    def performUnwind(self, stage, mgr):
        selector = self.selector
        selection = selector.finish()
        selection = [s[-1] for s in selection]

        mgr.finishSelector(selector, selection)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StageDebugPickMaterial(StagePickMaterial):
    gl = gl
    mask = gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT

    def __init__(self, usePickMatrix=False):
        StagePickMaterial.__init__(self)
        self.usePickMatrix = usePickMatrix

    def bind(self, stage, res, mgr):
        return [self.partial(self.perform, stage, mgr)]
    def perform(self, stage, mgr):
        gl = self.gl
        selector = self.selector
        selector.start()
        selector.finish()

        gl.glClear(self.mask)

        mgr.startSelector(selector)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        vpbox = stage.box.astype(int).tolist()
        if self.usePickMatrix:
            selector.pickMatrix(mgr.selectPos, mgr.selectSize, vpbox)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def bindUnwind(self, stage, res, mgr):
        return [self.partial(self.performUnwind, stage, mgr)]
    def performUnwind(self, stage, mgr):
        if not self.usePickMatrix:
            gl.glLoadIdentity()
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()

            x1, y1 = stage.box.pos
            x2, y2 = stage.box.corner
            gl.glOrtho(x1, x2, y1, y2, -10, 10)

            gl.glColor4ub(255,128,128,128)
            (x, y), (w, h), m = mgr.selectPos, mgr.selectSize, 5
            gl.glRectf(x-m*w, y-m*h, x+m*w, y+m*h)

            gl.glLoadIdentity()
            gl.glMatrixMode(gl.GL_MODELVIEW)

        mgr.finishSelector(self.selector, [])
        mgr.debugView = True

