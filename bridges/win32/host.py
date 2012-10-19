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
from contextlib import contextmanager
import ctypes
from ctypes import windll
from ctypes.wintypes import BYTE, WORD, DWORD

from venster import windows, wtl
from venster.lib import form
from . import viewLoader

gdi = ctypes.windll.gdi32
wgl = ctypes.windll.opengl32

class PIXELFORMATDESCRIPTOR(ctypes.Structure):
    _fields_ = [
        ('nSize', WORD),
        ('nVersion', WORD),
        ('dwFlags', DWORD),
        ('iPixelType', BYTE),
        ('cColorBits', BYTE),
        ('cRedBits', BYTE),
        ('cRedShift', BYTE),
        ('cGreenBits', BYTE),
        ('cGreenShift', BYTE),
        ('cBlueBits', BYTE),
        ('cBlueShift', BYTE),
        ('cAlphaBits', BYTE),
        ('cAlphaShift', BYTE),
        ('cAccumBits', BYTE),
        ('cAccumRedBits', BYTE),
        ('cAccumGreenBits', BYTE),
        ('cAccumBlueBits', BYTE),
        ('cAccumAlphaBits', BYTE),
        ('cDepthBits', BYTE),
        ('cStencilBits', BYTE),
        ('cAuxBuffers', BYTE),
        ('iLayerType', BYTE),
        ('bReserved', BYTE),
        ('dwLayerMask', DWORD),
        ('dwVisibleMask', DWORD),
        ('dwDamageMask', DWORD),
    ]

class msg_handler(object):
    def __init__(self, msg, fn):
        self.msg = msg
        self.fn = fn
    def __install__(self, msgMap):
        msgMap._msg_map_[self.msg] = self.fn

class Win32HelixGLWindow(form.Form):
    # redraw on any sizing
    _window_class_style_ = form.Form._window_class_style_
    _window_class_style_ |= windows.CS_HREDRAW | windows.CS_VREDRAW

    _window_title_ = "Helix"
    _form_exit_ = form.EXIT_ONLASTDESTROY
    _form_menu_ = []

    def __init__(self):
        # duplicate msg map for dynamic bindEvt()
        self._msg_map_ = type(self._msg_map_)(self._msg_map_._msg_map_.values())
        super(Win32HelixGLWindow, self).__init__()

    def bindEvt(self, msg, fn):
        self._msg_map_.append(msg_handler(msg, fn))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def OnCreate(self, evt):
        super(Win32HelixGLWindow, self).OnCreate(evt)
        self._createGLContext()
    def OnClose(self, evt):
        super(Win32HelixGLWindow, self).OnClose(evt)
        self._releaseGLContext()

    _glrc = None
    def _createGLContext(self):
        pfd = PIXELFORMATDESCRIPTOR()
        pfd.nSize = ctypes.sizeof(pfd)
        pfd.nVersion = 1
        pfd.dwFlags = 0x25
        pfd.iPixelType = 0 # RGBA
        pfd.cColorBits = 24 # 3*8
        pfd.cDepthBits = 16
        pfd.iLayerType = 0 # Main Plane

        hdc = self.GetDC()
        try:
            fmt = gdi.ChoosePixelFormat(hdc, ctypes.byref(pfd))
            res = gdi.SetPixelFormat(hdc, fmt, ctypes.byref(pfd))

            self._glrc = wgl.wglCreateContext(hdc)
            wgl.wglMakeCurrent(hdc, self._glrc)
        finally:
            self.ReleaseDC(hdc)
    def _releaseGLContext(self):
        glrc = self._glrc
        if glrc is not None:
            self._glrc = None
            wgl.wglMakeCurrent(None, None)
            wgl.wglDeleteContext(glrc)


    @contextmanager
    def inDCContext(self):
        hdc = self.GetDC()
        try: yield hdc
        finally: self.ReleaseDC(hdc)

    @contextmanager
    def inCurrentContext(self):
        with self.inDCContext() as hdc:
            wgl.wglMakeCurrent(hdc, self._glrc)
            yield hdc
    def makeCurrentContext(self):
        with self.inDCContext() as hdc:
            wgl.wglMakeCurrent(hdc, self._glrc)

    def swapBuffers(self):
        with self.inDCContext() as hdc:
            gdi.SwapBuffers(hdc)

    def setContentSize(self, w, h):
        rect = self.windowRect
        cw,ch = self.clientRect.size
        w = rect.width + (w-cw)
        h = rect.height + (h-ch)
        self.MoveWindow(rect.left, rect.top, w, h, True)
        return self

class Win32HelixHost(object):
    def __init__(self, theater, options=None):
        self.theater = theater
        self._glwin = Win32HelixGLWindow()

        self._glwin.makeCurrentContext()
        self.printGLInfo()

        if self.theater is not None:
            self.TheaterHostViewLoader.load(self._glwin, options, self.theater)

    TheaterHostViewLoader = viewLoader.TheaterHostViewLoader

    def printGLInfo(self):
        import TG.ext.openGL.raw
        TG.ext.openGL.printGLInfo()

    def getGLContext(self):
        return self._glwin.openGLContext()

    def show(self, visible=True):
        if visible:
            self._glwin.ShowWindow()
        else: self.hide()
    def hide(self):
        self._glwin.ShowWindow(0)

    def resize(self, width, height):
        self._glwin.setContentSize(width, height)
    def centerAndSize(self, width=1024, height=768):
        self._glwin.setContentSize(width, height)
        self._glwin.CenterWindow()

    def close(self):
        self._glwin.SendMessage(windows.WM_CLOSE, 0, 0)
        del self._glwin

