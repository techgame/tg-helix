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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxMouseEventSource(wxEventSourceMixin):
    channelKey = 'mouse'

    def bindHost(self, glCanvas, options):
        glCanvas.Bind(wx.EVT_MOUSE_EVENTS, self.onEvtMouse)
        glCanvas.Bind(wx.EVT_MOUSE_CAPTURE_CHANGED, self.onEvtMouseCapture)
        glCanvas.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.onEvtMouseCapture)

    def onEvtMouse(self, evt):
        etype, ekind, btn = self.wxEtypeMap[evt.GetEventType()]
        info = self.newInfo(etype=etype, ekind=ekind)
        
        if btn:
            info.update(btn=btn, op=btn+'-'+ekind)

        if ekind == 'wheel':
            info.update(
                wheel=evt.GetWheelRotation(),
                wheelLinesPer=evt.GetLinesPerAction(),
                wheelIsPage=evt.IsPageScroll())

        if not self.addKeyMouseInfo(info, (evt.GetX(), evt.GetY()), evt):
            evt.Skip()
            return

        self.evtRoot.send(self.channelKey, info)
        self.checkCapture(info)
        if info.get('skip', False):
            evt.Skip()

    def onEvtMouseCapture(self, evt=None):
        if evt is None:
            key = ('acquire' if self._captureState else 'release')
        else: key = evt.GetEventType()

        etype, ekind, captured = self.wxCaptureEtypeMap[key]
        self._captureState = captured
        info = self.newInfo(etype=etype, ekind=ekind, captured=captured)

        if not self.addKeyMouseInfo(info):
            evt.Skip()
            return

        self.evtRoot.send(self.channelKey, info)

        if evt is not None:
            if info.get('skip', True):
                evt.Skip()

    _captureState = False
    def checkCapture(self, info):
        capture = bool(info.get('capture', info.buttons))

        if capture != self._captureState:
            self._captureState = capture
            try:
                if capture:
                    self.glCanvas.CaptureMouse()
                else: 
                    self.glCanvas.ReleaseMouse()
            except wx.PyAssertionError:
                pass
            else:
                self.onEvtMouseCapture()

        return capture

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    wxCaptureEtypeMap = {
        'acquire': ('capture', 'acquire', True),
        'release': ('capture', 'release', False),
        wx.wxEVT_MOUSE_CAPTURE_LOST: ('capture', 'lost', False),
        wx.wxEVT_MOUSE_CAPTURE_CHANGED: ('capture', 'changed', False),
    }

    wxEtypeMap = {
        wx.wxEVT_ENTER_WINDOW: ('window', 'enter', None),
        wx.wxEVT_LEAVE_WINDOW: ('window', 'leave', None),

        wx.wxEVT_MOTION: ('motion', 'pos', None),
        wx.wxEVT_MOUSEWHEEL: ('motion', 'wheel', None),

        wx.wxEVT_LEFT_UP: ('button', 'up', 'left'),
        wx.wxEVT_LEFT_DOWN: ('button', 'down', 'left'),
        wx.wxEVT_LEFT_DCLICK: ('button', 'dclick', 'left'),

        wx.wxEVT_RIGHT_UP: ('button', 'up', 'right'),
        wx.wxEVT_RIGHT_DOWN: ('button', 'down', 'right'),
        wx.wxEVT_RIGHT_DCLICK: ('button', 'dclick', 'right'),

        wx.wxEVT_MIDDLE_UP: ('button', 'up', 'middle'),
        wx.wxEVT_MIDDLE_DOWN: ('button', 'down', 'middle'),
        wx.wxEVT_MIDDLE_DCLICK: ('button', 'dclick', 'middle'),
    }

