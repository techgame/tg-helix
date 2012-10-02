#!/usr/bin/env python
# -*- coding: utf-8 -*- vim: set ts=4 sw=4 expandtab
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2012  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

import sys
import Cocoa
from . import viewLoader

class EventEmitter(object):
    def __init__(self):
        self._map = {}
    def bind(self, key, fn):
        self._map[key] = fn
    def emit(self, key, *args):
        fn = self._map.get(key)
        if fn is not None:
            try: fn(*args)
            except Exception:
                sys.excepthook(*sys.exc_info())

class CocoaHelixGLView(Cocoa.NSOpenGLView):
    pixelFormatAttributes = [
        Cocoa.NSOpenGLPFAMPSafe, Cocoa.NSOpenGLPFADoubleBuffer,
        Cocoa.NSOpenGLPFAColorSize, 24, Cocoa.NSOpenGLPFAAlphaSize, 8,
        Cocoa.NSOpenGLPFADepthSize, 24, Cocoa.NSOpenGLPFAStencilSize, 8]

    def initWithFrame_(self, frameRect):
        self.events = EventEmitter()
        return Cocoa.NSOpenGLView.initWithFrame_pixelFormat_(self, frameRect,
            Cocoa.NSOpenGLPixelFormat.alloc().initWithAttributes_(self.pixelFormatAttributes))
    
    _drawLocked = False
    def invalidateGLView(self):
        if not self._drawLocked:
            self.setNeedsDisplay_(True)
        
    def drawRect_(self, rect):
        self._drawLocked = True
        self.events.emit('paint', rect)
        self._drawLocked = False
    def prepareOpenGL(self):
        self.events.emit('prepareOpenGL')
    def reshape(self):
        self.events.emit('reshape')

    def acceptsFirstResponder(self): return True

    def mouseEntered_(self, evt):
        self.events.emit('mouse', evt, 'window', 'enter')
    def mouseExited_(self, evt):
        self.events.emit('mouse', evt, 'window', 'leave')

    def mouseMoved_(self, evt):
        self.events.emit('mouse', evt, 'motion', 'pos')
    def mouseDragged_(self, evt):
        self.events.emit('mouse', evt, 'motion', 'pos')
    def rightMouseDragged_(self, evt):
        self.events.emit('mouse', evt, 'motion', 'pos')
    def otherMouseDragged_(self, evt):
        self.events.emit('mouse', evt, 'motion', 'pos')
    def scrollWheel_(self, evt):
        self.events.emit('mouse', evt, 'motion', 'wheel')

    def mouseDown_(self, evt):
        self.events.emit('mouse', evt, 'button', 'down', 'left')
    def mouseUp_(self, evt):
        self.events.emit('mouse', evt, 'button', 'up', 'left')

    def rightMouseDown_(self, evt):
        self.events.emit('mouse', evt, 'button', 'down', 'right')
    def rightMouseUp_(self, evt):
        self.events.emit('mouse', evt, 'button', 'up', 'right')

    def otherMouseDown_(self, evt):
        self.events.emit('mouse', evt, 'button', 'down', 'middle')
    def otherMouseUp_(self, evt):
        self.events.emit('mouse', evt, 'button', 'up', 'middle')

    def keyDown_(self, evt):
        self.events.emit('key', evt, 'key', 'down')
    def keyUp_(self, evt):
        self.events.emit('key', evt, 'key', 'up')


class CocoaHelixGLWindow(Cocoa.NSWindow):
    def initEx_(self, opt={}):
        frameRect = Cocoa.NSMakeRect(opt.pop('left',200), opt.pop('bottom', 200), opt.pop('width', 1280), opt.pop('height', 800))
        flags = opt.pop('flags', (Cocoa.NSResizableWindowMask | Cocoa.NSClosableWindowMask | Cocoa.NSTitledWindowMask))
        self = self.initWithContentRect_styleMask_backing_defer_(
                frameRect, flags, Cocoa.NSBackingStoreBuffered, False)
        self.setTitle_(opt.pop('title', 'Helix'))
        self.setReleasedWhenClosed_(True)

        glview = opt.pop('GLView', CocoaHelixGLView).alloc()
        self.glview = glview = glview.initWithFrame_(frameRect)
        self.setContentView_(self.glview)
        return self
    def isRestorable(self):
        return False

class CocoaHelixHost(object):
    def __init__(self, theater, options=None):
        self.theater = theater

        self._glwin = CocoaHelixGLWindow.alloc().initEx_()
        self._glview = self._glwin.glview

        self.getGLContext().makeCurrentContext()
        self.printGLInfo()

        if self.theater is not None:
            self.TheaterHostViewLoader.load(self._glview, options, self.theater)

    TheaterHostViewLoader = viewLoader.TheaterHostViewLoader

    def printGLInfo(self):
        import TG.ext.openGL.raw
        TG.ext.openGL.printGLInfo()

    def getGLContext(self):
        return self._glview.openGLContext()

    def show(self, visible=True):
        if visible:
            self._glwin.makeKeyAndOrderFront_(None)
        else: self.hide()
    def hide(self):
        self._glwin.orderOut_(None)

    def centerAndSize(self, width=1024, height=768):
        self._glwin.setContentSize_(Cocoa.NSMakeSize(w,h))
        self._glwin.center()

    def close(self):
        self._glwin.close()
        del self._glwin
        del self._glview

