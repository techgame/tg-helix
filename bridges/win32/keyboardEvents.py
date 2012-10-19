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

windows.WM_CHAR = windows.WM_KEYUP+1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Win32KeyboardEventSource(Win32EventSourceMixin):
    channelKey = 'key'

    def bindHost(self, glwin, options):
        for msgKey in self.etypeMap:
            glwin.bindEvt(msgKey, self.onEvtKey)
        glwin.SetFocus()

    def onEvtKey(self, tgt, evt):
        etype, ekind = self.etypeMap[evt.nMsg]
        if ekind == 'char':
            unikey = evt.wParam
            keyCode = None
        else:
            unikey = None
            keyCode = evt.wParam

        uchar = (unichr(unikey) if unikey else u'')
        token = self.kTranslate.get(keyCode, uchar)

        info = self.newInfo(etype=etype, ekind=ekind)
        info.update(ukey=unikey, uchar=uchar, token=token)
        if not self.addKeyMouseInfo(info, evt):
            return

        self.evtRoot.send(self.channelKey, info)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    etypeMap = {
        windows.WM_KEYDOWN: ('key', 'down', ),
        windows.WM_KEYUP: ('key', 'up', ),
        windows.WM_CHAR: ('key', 'char', ),
    }

    kTranslate = {
        0x01: 'lbutton', 0x02: 'rbutton', 0x04: 'mbutton', 0x05: 'xbutton1', 0x06: 'xbutton2',
        0x03: 'cancel', 0x08: 'back', 0x09: 'tab', 0x0c: 'clear', 0x0d: 'return',
        0x10: 'shift', 0x11: 'control', 0x12: 'alt',
        0x13: 'pause', 0x14: 'capital',
        0x15: 'hangul', 0x17: 'junja', 0x18: 'final', 0x19: 'hanja', 0x19: 'kanji',
        0x1b: 'escape',
        0x1c: 'convert', 0x1d: 'nonconvert',
        0x1e: 'accept', 0x1f: 'modechange',
        0x20: 'space',
        0x21: 'prior', 0x22: 'next', 0x23: 'end', 0x24: 'home',
        0x25: 'left', 0x26: 'up', 0x27: 'right', 0x28: 'down',

        0x29: 'select', 0x2a: 'print',
        0x2b: 'execute', 0x2c: 'snapshot',
        0x2d: 'insert', 0x2e: 'delete',
        0x2f: 'help',
        0x5b: 'lwin', 0x5c: 'rwin',
        0x5d: 'apps', 0x5f: 'sleep',

        0x60: 'numpad0', 0x61: 'numpad1',
        0x62: 'numpad2', 0x63: 'numpad3',
        0x64: 'numpad4', 0x65: 'numpad5',
        0x66: 'numpad6', 0x67: 'numpad7',
        0x68: 'numpad8', 0x69: 'numpad9',

        0x6a: 'multiply', 0x6b: 'add',
        0x6c: 'separator', 0x6d: 'subtract',
        0x6e: 'decimal', 0x6f: 'divide',

        0x70: 'f1', 0x71: 'f2', 0x72: 'f3', 0x73: 'f4',
        0x74: 'f5', 0x75: 'f6', 0x76: 'f7', 0x77: 'f8',
        0x78: 'f9', 0x79: 'f10', 0x7a: 'f11', 0x7b: 'f12',
        0x7c: 'f13', 0x7d: 'f14', 0x7e: 'f15', 0x7f: 'f16',
        0x80: 'f17', 0x81: 'f18', 0x82: 'f19', 0x83: 'f20',
        0x84: 'f21', 0x85: 'f22', 0x86: 'f23', 0x87: 'f24',
        0x90: 'numlock', 0x91: 'scroll' }
