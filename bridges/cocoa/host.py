#!/usr/bin/env python
# -*- coding: utf-8 -*- vim: set ts=4 sw=4 expandtab
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2012  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

import Cocoa
from . import viewLoader

class CocoaHelixGLView(Cocoa.NSOpenGLView):
    pixelFormatAttributes = [
        Cocoa.NSOpenGLPFAMPSafe, Cocoa.NSOpenGLPFADoubleBuffer,
        Cocoa.NSOpenGLPFAColorSize, 24, Cocoa.NSOpenGLPFAAlphaSize, 8,
        Cocoa.NSOpenGLPFADepthSize, 24, Cocoa.NSOpenGLPFAStencilSize, 8]

    def initWithFrame_(self, frameRect):
        return Cocoa.NSOpenGLView.initWithFrame_pixelFormat_(self, frameRect,
            Cocoa.NSOpenGLPixelFormat.alloc().initWithAttributes_(self.pixelFormatAttributes))
    
    if 0:
        def drawRect_(self, ((x, y), (w, h))):
            print 'drawRect', [x,y,w,h]
        def prepareOpenGL(self):
            print 'prepareOpenGL'
        def reshape(self):
            print 'reshape'

class CocoaHelixGLWindow(Cocoa.NSWindow):
    def initEx_(self, opt={}):
        frameRect = Cocoa.NSMakeRect(opt.pop('left',200), opt.pop('bottom', 200), opt.pop('width', 1280), opt.pop('height', 800))
        flags = opt.pop('flags', (Cocoa.NSResizableWindowMask | Cocoa.NSClosableWindowMask | Cocoa.NSTitledWindowMask))
        self = self.initWithContentRect_styleMask_backing_defer_(
                frameRect, flags, Cocoa.NSBackingStoreBuffered, False)
        self.setTitle_(opt.pop('title', 'Helix'))

        glview = opt.pop('GLView', CocoaHelixGLView).alloc()
        self.glview = glview = glview.initWithFrame_(frameRect)
        self.setContentView_(self.glview)
        return self

class CocoaHelixHost(object):
    def __init__(self, theater, options=None):
        self.theater = theater

        r = {}
        if options is not None:
            r.update(options)
        self.options = r

        self._glwin = CocoaHelixGLWindow.alloc().initEx_()
        self._glview = self._glwin.glview

        self.getGLContext().makeCurrentContext()
        self.printGLInfo()

        if self.theater is not None:
            self.TheaterHostViewLoader.load(self._glview, self.options, self.theater)

    TheaterHostViewLoader = viewLoader.TheaterHostViewLoader

    def printGLInfo(self):
        import TG.ext.openGL.raw
        TG.ext.openGL.printGLInfo()

    def getGLContext(self):
        return self._glview.openGLContext()

    def show(self, visible=True):
        if visible:
            self._glwin.makeKeyAndOrderFront_(None)
        else: self._glwin.orderOut_(None)

    def adjPosition(self):
        w,h = self.options.get('size', (1024, 768))
        self._glwin.setContentSize_(Cocoa.NSMakeSize(w,h))
        self._glwin.center()

