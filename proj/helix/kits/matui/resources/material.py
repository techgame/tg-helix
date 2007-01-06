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

from __future__ import with_statement

from functools import partial

from TG.openGL.raw import gl

from .units import MatuiMaterialUnit

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Loader Mixin
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MaterialLoaderMixin(object):
    def nullMaterial(self):
        r = NullMaterial()
        return self.asResult(r)

    def debugMaterial(self, name):
        r = DebugMaterial(name)
        return self.asResult(r)

    def stageMaterialGroup(self):
        r = dict(
            render=StageRenderMaterial(),
            pick=StagePickMaterial(),
            resize=StageResizeMaterial(),
            )
        return self.asResult(r)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Material Resources
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiMaterial(MatuiMaterialUnit):
    def bind(self, actor, res):
        return partial(self.perform, actor, res)

    def perform(self, actor, res, mgr):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

Material = MatuiMaterial

class NullMaterial(MatuiMaterial):
    def perform(self, actor, res, mgr):
        pass

class DebugMaterial(MatuiMaterial):
    def __init__(self, name):
        self.name = name
    def perform(self, actor, res, mgr):
        print '%s(%s):' % (self.__class__.__name__, self.name)
        print '  - %r' % (actor,)
        print '  - res: %s' % (', '.join(res.keys()),)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StageRenderMaterial(MatuiMaterial):
    mask = gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT
    glClear = staticmethod(gl.glClear)

    def perform(self, stage, res, mgr):
        self.glClear(self.mask)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glMatrixMode(gl.GL_MODELVIEW)

class StageResizeMaterial(MatuiMaterial):
    glViewport = staticmethod(gl.glViewport)
    def perform(self, stage, res, mgr):
        w, h = mgr.viewportSize
        stage.box.size[:2] = (w, h)
        self.glViewport(0, 0, w, h)

class StagePickMaterial(MatuiMaterial):
    def perform(self, stage, res, mgr):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        #self.renderPickMatrix(vpbox)
        gl.glMatrixMode(gl.GL_MODELVIEW)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Selection Visitor
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#class MatuiNameSelector(NameSelector):
#    def __init__(self, info, pos, *args, **kw):
#        self.info = info
#        pos = Vector(pos+(0.,))
#        NameSelector.__init__(self, pos, *args, **kw)

#    def renderProjection(self, vpbox):
#        gl.glMatrixMode(gl.GL_PROJECTION)
#        gl.glLoadIdentity()
#        self.renderPickMatrix(vpbox)
#        gl.glMatrixMode(gl.GL_MODELVIEW)

#    def _processHits(self, hitRecords, namedItems):
#        selection = NameSelector._processHits(self, hitRecords, namedItems)
#        selection.sort()
#        return [s[-1] for s in selection]

#class MatuiSelectionVisitor(MatuiVisitor):
#    MatuiSelectorFactory = MatuiNameSelector

#    def pick(self, pos, info):
#        selector = self.MatuiSelectorFactory(info, pos)

#        with selector:
#            self.renderPick(selector)
#            for view in self.views:
#                view.renderPick(selector)
#        return selector.selection

