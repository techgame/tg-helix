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

from .common import wx, wxEventSourceMixin
from TG.helix.events.keyboardEvents import GLKeyboardEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxGLKeyboardEventSource(wxEventSourceMixin, GLKeyboardEventSource):
    def __init__(self, glCanvas):
        GLKeyboardEventSource.__init__(self)
        wxEventSourceMixin.__init__(self, glCanvas)
        glCanvas.Bind(wx.EVT_KEY_DOWN, self.onEvtKey)
        glCanvas.Bind(wx.EVT_KEY_UP, self.onEvtKey)
        glCanvas.Bind(wx.EVT_CHAR, self.onEvtKey)

    def onEvtKey(self, evt):
        etype, = self.wxEtypeMap[evt.GetEventType()]

        unikey = evt.GetUnicodeKey()

        info = self.newInfo(
            etype=etype,
            ukey=unikey,
            uchar=(unichr(unikey) if unikey else u''),
            modifiers=((evt.AltDown() and 0x1) | (evt.ControlDown() and 0x2) | (evt.ShiftDown() and 0x4) | (evt.MetaDown() and 0x8)),
            )
        info.update(self._globalMouseInfo())

        if etype == 'char':
            info['token'] = self.wxkTranslate.get(evt.GetKeyCode())

        if not self.sendKey(info):
            evt.Skip()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    wxEtypeMap = {
        wx.wxEVT_KEY_DOWN: ('down', ),
        wx.wxEVT_KEY_UP: ('up', ),
        wx.wxEVT_CHAR: ('char', ),
    }

    wxkTranslate = {
        wx.WXK_BACK: 'back',
        wx.WXK_TAB: 'tab',
        wx.WXK_RETURN: 'return',
        wx.WXK_ESCAPE: 'escape',
        wx.WXK_SPACE: 'space',
        wx.WXK_DELETE: 'delete',
        wx.WXK_START: 'start',
        wx.WXK_LBUTTON: 'lbutton',
        wx.WXK_RBUTTON: 'rbutton',
        wx.WXK_CANCEL: 'cancel',
        wx.WXK_MBUTTON: 'mbutton',
        wx.WXK_CLEAR: 'clear',
        wx.WXK_SHIFT: 'shift',
        wx.WXK_ALT: 'alt',
        wx.WXK_CONTROL: 'control',
        wx.WXK_MENU: 'menu',
        wx.WXK_PAUSE: 'pause',
        wx.WXK_CAPITAL: 'capital',
        wx.WXK_PRIOR: 'prior',
        wx.WXK_NEXT: 'next',
        wx.WXK_END: 'end',
        wx.WXK_HOME: 'home',
        wx.WXK_LEFT: 'left',
        wx.WXK_UP: 'up',
        wx.WXK_RIGHT: 'right',
        wx.WXK_DOWN: 'down',
        wx.WXK_SELECT: 'select',
        wx.WXK_PRINT: 'print',
        wx.WXK_EXECUTE: 'execute',
        wx.WXK_SNAPSHOT: 'snapshot',
        wx.WXK_INSERT: 'insert',
        wx.WXK_HELP: 'help',
        wx.WXK_NUMPAD0: 'numpad0',
        wx.WXK_NUMPAD1: 'numpad1',
        wx.WXK_NUMPAD2: 'numpad2',
        wx.WXK_NUMPAD3: 'numpad3',
        wx.WXK_NUMPAD4: 'numpad4',
        wx.WXK_NUMPAD5: 'numpad5',
        wx.WXK_NUMPAD6: 'numpad6',
        wx.WXK_NUMPAD7: 'numpad7',
        wx.WXK_NUMPAD8: 'numpad8',
        wx.WXK_NUMPAD9: 'numpad9',
        wx.WXK_MULTIPLY: 'multiply',
        wx.WXK_ADD: 'add',
        wx.WXK_SEPARATOR: 'separator',
        wx.WXK_SUBTRACT: 'subtract',
        wx.WXK_DECIMAL: 'decimal',
        wx.WXK_DIVIDE: 'divide',
        wx.WXK_F1: 'f1',
        wx.WXK_F2: 'f2',
        wx.WXK_F3: 'f3',
        wx.WXK_F4: 'f4',
        wx.WXK_F5: 'f5',
        wx.WXK_F6: 'f6',
        wx.WXK_F7: 'f7',
        wx.WXK_F8: 'f8',
        wx.WXK_F9: 'f9',
        wx.WXK_F10: 'f10',
        wx.WXK_F11: 'f11',
        wx.WXK_F12: 'f12',
        wx.WXK_F13: 'f13',
        wx.WXK_F14: 'f14',
        wx.WXK_F15: 'f15',
        wx.WXK_F16: 'f16',
        wx.WXK_F17: 'f17',
        wx.WXK_F18: 'f18',
        wx.WXK_F19: 'f19',
        wx.WXK_F20: 'f20',
        wx.WXK_F21: 'f21',
        wx.WXK_F22: 'f22',
        wx.WXK_F23: 'f23',
        wx.WXK_F24: 'f24',
        wx.WXK_NUMLOCK: 'numlock',
        wx.WXK_SCROLL: 'scroll',
        wx.WXK_PAGEUP: 'pageup',
        wx.WXK_PAGEDOWN: 'pagedown',
        wx.WXK_NUMPAD_SPACE: 'numpad_space',
        wx.WXK_NUMPAD_TAB: 'numpad_tab',
        wx.WXK_NUMPAD_ENTER: 'numpad_enter',
        wx.WXK_NUMPAD_F1: 'numpad_f1',
        wx.WXK_NUMPAD_F2: 'numpad_f2',
        wx.WXK_NUMPAD_F3: 'numpad_f3',
        wx.WXK_NUMPAD_F4: 'numpad_f4',
        wx.WXK_NUMPAD_HOME: 'numpad_home',
        wx.WXK_NUMPAD_LEFT: 'numpad_left',
        wx.WXK_NUMPAD_UP: 'numpad_up',
        wx.WXK_NUMPAD_RIGHT: 'numpad_right',
        wx.WXK_NUMPAD_DOWN: 'numpad_down',
        wx.WXK_NUMPAD_PRIOR: 'numpad_prior',
        wx.WXK_NUMPAD_PAGEUP: 'numpad_pageup',
        wx.WXK_NUMPAD_NEXT: 'numpad_next',
        wx.WXK_NUMPAD_PAGEDOWN: 'numpad_pagedown',
        wx.WXK_NUMPAD_END: 'numpad_end',
        wx.WXK_NUMPAD_BEGIN: 'numpad_begin',
        wx.WXK_NUMPAD_INSERT: 'numpad_insert',
        wx.WXK_NUMPAD_DELETE: 'numpad_delete',
        wx.WXK_NUMPAD_EQUAL: 'numpad_equal',
        wx.WXK_NUMPAD_MULTIPLY: 'numpad_multiply',
        wx.WXK_NUMPAD_ADD: 'numpad_add',
        wx.WXK_NUMPAD_SEPARATOR: 'numpad_separator',
        wx.WXK_NUMPAD_SUBTRACT: 'numpad_subtract',
        wx.WXK_NUMPAD_DECIMAL: 'numpad_decimal',
        wx.WXK_NUMPAD_DIVIDE: 'numpad_divide',
        wx.WXK_WINDOWS_LEFT: 'windows_left',
        wx.WXK_WINDOWS_RIGHT: 'windows_right',
        wx.WXK_WINDOWS_MENU: 'windows_menu',
        wx.WXK_COMMAND: 'command',
        wx.WXK_SPECIAL1: 'special1',
        wx.WXK_SPECIAL2: 'special2',
        wx.WXK_SPECIAL3: 'special3',
        wx.WXK_SPECIAL4: 'special4',
        wx.WXK_SPECIAL5: 'special5',
        wx.WXK_SPECIAL6: 'special6',
        wx.WXK_SPECIAL7: 'special7',
        wx.WXK_SPECIAL8: 'special8',
        wx.WXK_SPECIAL9: 'special9',
        wx.WXK_SPECIAL10: 'special10',
        wx.WXK_SPECIAL11: 'special11',
        wx.WXK_SPECIAL12: 'special12',
        wx.WXK_SPECIAL13: 'special13',
        wx.WXK_SPECIAL14: 'special14',
        wx.WXK_SPECIAL15: 'special15',
        wx.WXK_SPECIAL16: 'special16',
        wx.WXK_SPECIAL17: 'special17',
        wx.WXK_SPECIAL18: 'special18',
        wx.WXK_SPECIAL19: 'special19',
        wx.WXK_SPECIAL20: 'special20',
        }