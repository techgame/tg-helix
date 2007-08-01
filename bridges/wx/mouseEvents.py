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

        self.addKeyMouseInfo(info, (evt.GetX(), evt.GetY()), evt)

        self.evtRoot.send(self.channelKey, info)
        if info.get('skip', False):
            evt.Skip()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

