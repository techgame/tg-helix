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

class qtHelixHost(QtOpenGL.QGLWidget, viewLoader.qtHostMixin):
    TheaterHostViewLoader = viewLoader.TheaterHostViewLoader

    def __init__(self, scene, parent=None):
        app = self.findApp()
        self.scene = scene
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

        if self.scene is not None:
            self.TheaterHostViewLoader.load(self, {}, self.scene)

    def _glApiReload(self):
        # Reload the opengl raw api to support windows
        if sys.platform.startswith('win'):
            import TG.ext.openGL.raw
            TG.ext.openGL.raw.apiReload()

    def printGLInfo(self):
        import TG.ext.openGL.raw
        TG.ext.openGL.printGLInfo()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _initQTWidget(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self)#, parent)
        glctx = self._createQGLContext(True)

        # helix handles the swappig of buffers
        self.setAutoBufferSwap(False)

    def _createQGLContext(self, setDefault=True):
        fmt = self._describeQTFormat()
        ctx = QtOpenGL.QGLContext(fmt, self)
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

        fmt.setSwapInterval(0) # vsync disabled

        fmt.setAccum(False)
        fmt.setStereo(False)
        return fmt

HelixHost = qtHelixHost

