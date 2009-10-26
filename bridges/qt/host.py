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
from .libqt import QtCore, QtGui, QtOpenGL
from . import viewLoader

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtHelixMixin(viewLoader.qtHostMixin):
    TheaterHostViewLoader = viewLoader.TheaterHostViewLoader

    def __init__(self, helixScene, parent=None):
        app = self.findApp()
        self.helixScene = helixScene
        self._initQTWidget(parent)
        self.bindScene()

    def findApp(self, orCreate=True):
        qApp = QtGui.qApp.instance()
        if qApp is None:
            if orCreate:
                qApp = QtGui.QApplication(sys.argv)
            else:
                raise RuntimeError("QApplication must be created before using QGLWidget")
        return qApp

    def run(self):
        return self.findApp().exec_()

    def bindScene(self):
        self.makeCurrent()

        self._glApiReload()
        self.printGLInfo()

        if self.helixScene is not None:
            self.TheaterHostViewLoader.load(self, {}, self.helixScene)

    def _glApiReload(self):
        # Reload the opengl raw api to support windows
        if sys.platform.startswith('win'):
            import TG.ext.openGL.raw
            TG.ext.openGL.raw.apiReload()

    def printGLInfo(self):
        import TG.ext.openGL.raw
        TG.ext.openGL.printGLInfo()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getGLWidget(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def _initQTWidget(self, parent=None):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def _createQGLContext(self, setDefault=True, glWidget=None):
        if glWidget is None:
            glWidget = self.getGLWidget()
        fmt = self._describeQTFormat()
        ctx = QtOpenGL.QGLContext(fmt, glWidget)
        if not ctx.create():
            raise RuntimeError("Could not create a valid Qt OpenGL Context")

        if setDefault:
            # get the closest matching format
            fmt = ctx.format()
            QtOpenGL.QGLFormat.setDefaultFormat(fmt)
        return ctx

    def _describeQTFormat(self):
        fmt = QtOpenGL.QGLFormat()
        fmt.setAlpha(True)
        fmt.setDepth(True)
        fmt.setDoubleBuffer(True)
        fmt.setRgba(True)
        fmt.setStencil(True)

        #fmt.setSwapInterval(0) # vsync disabled

        fmt.setAccum(False)
        fmt.setStereo(False)
        return fmt

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtHelixGLWidgetHost(qtHelixMixin, QtOpenGL.QGLWidget):
    def getGLWidget(self):
        return self

    def _initQTWidget(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self._createQGLContext(True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtHelixQGraphicsScene(QtGui.QGraphicsScene):
    def drawBackground(self, painter, rect):
        pe = painter.paintEngine()
        assert pe.type() == pe.OpenGL, "Must use an OpenGL paint engine"

        if 1:
            from TG.ext.openGL.raw import gl
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glPushMatrix()
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glPushMatrix()
            gl.glPushAttrib(gl.GL_ALL_ATTRIB_BITS)

        self.paintGL()

        if 1:
            gl.glPopAttrib()
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glPopMatrix()
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glPopMatrix()

    def setHelixViewportDelegate(self, dgViewport):
        self.dgViewport = dgViewport
    def initializeGL(self):
        return self.dgViewport.initializeGL()
    def resizeGL(self, w, h):
        return self.dgViewport.resizeGL(w, h)
    def paintGL(self):
        return self.dgViewport.paintGL()

class qtHelixQGraphicsViewHost(qtHelixMixin, QtGui.QGraphicsView):
    QGraphicsSceneFactory = qtHelixQGraphicsScene

    def getGLWidget(self):
        return self._glWidget
    def makeCurrent(self):
        return self._glWidget.makeCurrent()

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

            self.makeCurrent()
            self.scene().resizeGL(r.width(), r.height())

        return QtGui.QGraphicsView.resizeEvent(self, evt)

qtHelixHost = qtHelixQGraphicsViewHost
#qtHelixHost = qtHelixGLWidgetHost
HelixHost = qtHelixHost

