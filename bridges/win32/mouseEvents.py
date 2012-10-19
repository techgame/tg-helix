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

import ctypes
from ctypes import wintypes
from .common import Win32EventSourceMixin
from venster import windows

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TRACKMOUSEEVENT(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('dwFlags', wintypes.DWORD),
        ('hwndTrack', wintypes.HWND),
        ('dwHoverTime', wintypes.DWORD)]

TrackMouseEvent = ctypes.windll.user32.TrackMouseEvent
TrackMouseEvent.argtypes = [ctypes.POINTER(TRACKMOUSEEVENT)]
TrackMouseEvent.restype = wintypes.BOOL

windows.WM_MOUSEWHEEL = 0x020A

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Win32MouseEventSource(Win32EventSourceMixin):
    channelKey = 'mouse'

    def bindHost(self, glwin, options):
        self._installMouseTracking(glwin)
        for msgMouse in self.etypeMap:
            glwin.bindEvt(msgMouse, self.onEvtMouse)
        glwin.bindEvt(windows.WM_CAPTURECHANGED, self.onEvtMouseCapture)

    def _installMouseTracking(self, glwin):
        tm = TRACKMOUSEEVENT()
        tm.cbSize = ctypes.sizeof(tm)
        tm.dwFlags = 0x3 # HOVER & LEAVE
        tm.hwndTrack = glwin.handle
        tm.dwHoverTime = 0 # no delay - handled internally
        return bool(TrackMouseEvent(ctypes.byref(tm)))

    def onEvtMouse(self, tgt, evt):
        etype, ekind, btn = self.etypeMap[evt.nMsg]
        info = self.newInfo(etype=etype, ekind=ekind)
        
        if btn:
            info.update(btn=btn, op=btn+'-'+ekind)

        if ekind == 'wheel':
            # wheel delta is in the high-order word
            rotation = int(evt.wParam>>16)
            if rotation&0x8000:
                # offset because it's negative
                rotation -= 0x10000
            info.update(wheel=rotation,
                wheelLinesPer=rotation/120,
                wheelIsPage=False)

        if not self.addKeyMouseInfo(info, evt): return

        self.evtRoot.send(self.channelKey, info)
        self.checkCapture(info)

    def onEvtMouseCapture(self, tgt=None, evt=None):
        if evt is None:
            key = ('acquire' if self._captureState else 'release')
        else: key = evt.nMsg

        etype, ekind, captured = self.captureEtypeMap[key]
        self._captureState = captured
        info = self.newInfo(etype=etype, ekind=ekind, captured=captured)

        if not self.addKeyMouseInfo(info): return
        self.evtRoot.send(self.channelKey, info)

    _captureState = False
    def checkCapture(self, info):
        capture = bool(info.get('capture', info.buttons))

        if capture != self._captureState:
            self._captureState = capture
            if capture:
                self.glwin.SetCapture()
            else: windows.ReleaseCapture()
            self.onEvtMouseCapture()

        return capture

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    captureEtypeMap = {
        'acquire': ('capture', 'acquire', True),
        'release': ('capture', 'release', False),
        windows.WM_CAPTURECHANGED: ('capture', 'changed', False),
    }

    etypeMap = {
        windows.WM_MOUSEHOVER: ('window', 'enter', None),
        windows.WM_MOUSELEAVE: ('window', 'leave', None),

        windows.WM_MOUSEMOVE: ('motion', 'pos', None),
        windows.WM_MOUSEWHEEL: ('motion', 'wheel', None),

        windows.WM_LBUTTONUP: ('button', 'up', 'left'),
        windows.WM_LBUTTONDOWN: ('button', 'down', 'left'),
        windows.WM_LBUTTONDBLCLK: ('button', 'dclick', 'left'),

        windows.WM_RBUTTONUP: ('button', 'up', 'right'),
        windows.WM_RBUTTONDOWN: ('button', 'down', 'right'),
        windows.WM_RBUTTONDBLCLK: ('button', 'dclick', 'right'),

        windows.WM_MBUTTONUP: ('button', 'up', 'middle'),
        windows.WM_MBUTTONDOWN: ('button', 'down', 'middle'),
        windows.WM_MBUTTONDBLCLK: ('button', 'dclick', 'middle'),
    }

