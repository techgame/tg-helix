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

from TG.helix.events.mouseEvents import MouseEventSource
from .common import wx, wxEventSourceMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxMouseEventSource(wxEventSourceMixin, MouseEventSource):
    buttonByBit = {
        0x1: 'left',
        0x2: 'right',
        0x4: 'middle',
        }
    modifierByBit = {
        0x1: 'alt',
        0x2: 'control',
        0x4: 'shift',
        0x8: 'meta',
        }

    def __init__(self, glCanvas, options):
        MouseEventSource.__init__(self)
        wxEventSourceMixin.__init__(self, glCanvas)
        glCanvas.Bind(wx.EVT_MOUSE_EVENTS, self.onEvtMouse)

    def onEvtMouse(self, evt):
        etype, srcBtn = self.wxEtypeMap[evt.GetEventType()]
        eoHeight = evt.GetEventObject().GetClientSize()[1]

        # mouseState is more accurate for combinations of buttons
        mouseState = wx.GetMouseState()
        info = self.newInfo(
                etype=etype,
                pos=(evt.GetX(), eoHeight - evt.GetY()), # change to bottom left orientation
                buttons=((mouseState.LeftDown() and 0x1) | (mouseState.RightDown() and 0x2) | (mouseState.MiddleDown() and 0x4)),
                modifiers=((evt.AltDown() and 0x1) | (evt.ControlDown() and 0x2) | (evt.ShiftDown() and 0x4) | (evt.MetaDown() and 0x8)),
                buttonSource=srcBtn,
                )

        if etype == 'wheel':
            info.update(
                wheel=evt.GetWheelRotation(),
                wheelLinesPer=evt.GetLinesPerAction(),
                wheelIsPage=evt.IsPageScroll())

        if not self.sendMouse(info):
            evt.Skip()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    wxEtypeMap = {
        wx.wxEVT_ENTER_WINDOW: ('enter', 0),
        wx.wxEVT_LEAVE_WINDOW: ('leave', 0),

        wx.wxEVT_MOTION: ('motion', 0),
        wx.wxEVT_MOUSEWHEEL: ('wheel', 0),

        wx.wxEVT_LEFT_UP: ('up', 0x1),
        wx.wxEVT_LEFT_DOWN: ('down', 0x1),
        wx.wxEVT_LEFT_DCLICK: ('dclick', 0x1),

        wx.wxEVT_RIGHT_UP: ('up', 0x2),
        wx.wxEVT_RIGHT_DOWN: ('down', 0x2),
        wx.wxEVT_RIGHT_DCLICK: ('dclick', 0x2),

        wx.wxEVT_MIDDLE_UP: ('up', 0x4),
        wx.wxEVT_MIDDLE_DOWN: ('down', 0x4),
        wx.wxEVT_MIDDLE_DCLICK: ('dclick', 0x4),
    }

