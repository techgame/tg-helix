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
import warnings
from .libqt import QtCore, QtGui, QtOpenGL
from . import viewLoader

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtGLDelegateMixin(object):
    # viewport delegate
    dgViewport = None

    def setHelixViewportDelegate(self, dgViewport):
        self.dgViewport = dgViewport
    def initializeGL(self):
        return self.dgViewport.initializeGL()
    def resizeGL(self, w, h):
        return self.dgViewport.resizeGL(w, h)
    def paintGL(self):
        return self.dgViewport.paintGL()

class qtEventDispatchMixin(object):
    _eventRegistry = None
    def getEventRegistry(self):
        reg = self._eventRegistry
        if reg is None:
            reg = {}
            self._eventRegistry = reg
        return reg
    eventRegistry = property(getEventRegistry)

    def bindEvent(self, key, fn):
        self.eventRegistry[key] = fn

    def _dispatchRegisteredEvent(self, evt):
        et = evt.type(); ek = evt.__class__
        reg = self.eventRegistry
        fns = []
        for key in [(et, ek), et, ek]:
            fn = reg.get(key)
            if fn is not None:
                fns.append(fn)

        if fns:
            for fn in fns:
                r = fn(evt)
                if r: 
                    return r
        return False

    def event(self, evt):
        r0 = self._dispatchRegisteredEvent(evt)
        r1 = super(qtEventDispatchMixin, self).event(evt)
        if evt.isAccepted(): 
            return r1
        return r0 or False


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Qt Helix Mixin Class
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtHelixMixin(qtEventDispatchMixin):
    TheaterHostViewLoader = None

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
        self.getGLWidget().makeCurrent()

        self._glApiReload()
        self.printGLInfo()

        self.setHelixScene(self.helixScene)

    def setHelixScene(self, helixScene):
        self.getGLWidget().makeCurrent()
        self.helixScene = helixScene
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
            warnings.warn("Unable to create requested OpenGL context.  Proceeding with default")
            return None

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Here's the actual combination of QtOpenGL and QGLWidget
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtHelixGLWidgetHost(qtGLDelegateMixin, qtHelixMixin, QtOpenGL.QGLWidget):
    TheaterHostViewLoader = viewLoader.TheaterHostViewLoader

    def getGLWidget(self):
        return self

    def _initQTWidget(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self._createQGLContext(True)


qtHelixHost = qtHelixGLWidgetHost
HelixHost = qtHelixHost

