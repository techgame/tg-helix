# -*- coding: utf-8 -*- vim: set ts=4 sw=4 expandtab
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2012  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

import ctypes
from ctypes import wintypes
from venster import windows
from TG.helix.actors.events import EventSource

GetKeyState = ctypes.windll.user32.GetKeyState
GetKeyState.argtypes = [wintypes.INT]
GetKeyState.restype = wintypes.SHORT
GetAsyncKeyState = ctypes.windll.user32.GetAsyncKeyState
GetAsyncKeyState.argtypes = [wintypes.INT]
GetAsyncKeyState.restype = wintypes.SHORT

def keySyncState(vkey, name=None): return bool(GetKeyState(vkey) >> 1)
def keyAsyncState(vkey, name=None): return bool(GetAsyncKeyState(vkey) >> 1)

def btnSyncState(vkey, name=None): return bool(GetKeyState(vkey) >> 1)
def btnAsyncState(vkey, name=None): return bool(GetAsyncKeyState(vkey) >> 1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Win32EventSourceMixin(EventSource):
    def __init__(self, glwin, options, theater):
        self.glwin = glwin
        self.evtRootSetup(theater.evtRoot)
        self.bindHost(glwin, options)

    def __nonzero__(self):
        return bool(self.glwin)

    def bindHost(self, glwin, options):
        pass

    buttonMap = {0x1:'left', 0x2:'right', 0x4:'middle', 0x5:'button4', 0x6:'button5'}
    modifierMap = {0x10:'shift', 0x11:'control', 0x12:'alt', 0x5b:'meta', 0x5c:'meta'}

    def addKeyMouseInfo(self, info, evt=None):
        win = self.glwin
        if not win or not win.IsWindowVisible() or win.IsIconic():
            return None

        rect = win.clientRect
        pt = windows.POINT()
        windows.GetCursorPos(ctypes.byref(pt))
        win.ScreenToClient(pt)
        pos = pt.x, rect.height-pt.y

        if evt is not None:
            modifiers = set(v for k,v in self.modifierMap.items() if keySyncState(k,v))
            buttons = set(v for k,v in self.buttonMap.items() if btnSyncState(k,v))
        else:
            modifiers = set(v for k,v in self.modifierMap.items() if keyAsyncState(k,v))
            buttons = set(v for k,v in self.buttonMap.items() if btnAsyncState(k,v))

        if 0:
            print '\rpos:', pos,
            print 'modifiers:', modifiers,
            print 'buttons:', buttons,
            print ' '*40,
            #print
        info.update(pos=pos, modifiers=modifiers, buttons=buttons, viewSize=rect.size)
        return info

