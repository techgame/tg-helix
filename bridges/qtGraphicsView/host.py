##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2009  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys, os
from ..qt.host import qtHelixMixin, qtGLDelegateMixin, qtEventDispatchMixin
from ..qt.libqt import QtCore, QtGui, QtOpenGL
from . import viewLoader

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

paintEngines = [QtGui.QPaintEngine.OpenGL, QtGui.QPaintEngine.OpenGL2]

class qtHelixQGraphicsScene(qtEventDispatchMixin, QtGui.QGraphicsScene):
    _paintEngines = paintEngines
    def drawBackground(self, painter, rect):
        pe = painter.paintEngine()
        assert pe.type() in self._paintEngines, "Must use an OpenGL paint engine"

        painter.beginNativePainting()
        self._glKeepState(True)
        self.paintGL()
        self._glKeepState(False)
        painter.endNativePainting()

    def _glKeepState(self, push):
        gl = self.gl
        if push:
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glPushMatrix()
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glPushMatrix()
            gl.glPushAttrib(gl.GL_ALL_ATTRIB_BITS)
        else:
            gl.glPopAttrib()
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glPopMatrix()
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glPopMatrix()

    def setHelixViewportDelegate(self, dgViewport):
        from TG.ext.openGL.raw import gl
        self.gl = gl
        self.dgViewport = dgViewport

    def initializeGL(self):
        return self.dgViewport.initializeGL()
    def resizeGL(self, w, h):
        return self.dgViewport.resizeGL(w, h)
    def paintGL(self):
        return self.dgViewport.paintGL()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtHelixQGraphicsViewHost(qtHelixMixin, QtGui.QGraphicsView):
    TheaterHostViewLoader = viewLoader.TheaterHostViewLoader
    QGraphicsSceneFactory = qtHelixQGraphicsScene

    def getGLWidget(self):
        return self._glWidget

    def _initQTWidget(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)
        self._glWidget = QtOpenGL.QGLWidget()
        self._createQGLContext(True, self._glWidget)
        self.setViewport(self._glWidget)
        self.setViewportUpdateMode(self.FullViewportUpdate)

        self.setScene(self.QGraphicsSceneFactory())

    def setHelixViewportDelegate(self, dgViewport):
        self.scene().setHelixViewportDelegate(dgViewport)

    def resizeEvent(self, evt):
        if self.scene():
            r = QtCore.QRect(QtCore.QPoint(0, 0), evt.size())
            r = QtCore.QRectF(r)
            self.scene().setSceneRect(r)

            self.getGLWidget().makeCurrent()
            self.scene().resizeGL(r.width(), r.height())

        return QtGui.QGraphicsView.resizeEvent(self, evt)

qtHelixHost = qtHelixQGraphicsViewHost
HelixHost = qtHelixHost

