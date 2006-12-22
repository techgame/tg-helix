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
from TG.helix.events.mouseEvents import GLMouseEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxGLMouseEventSource(wxEventSourceMixin, GLMouseEventSource):
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

    def __init__(self, glCanvas):
        GLMouseEventSource.__init__(self)
        wxEventSourceMixin.__init__(self, glCanvas)
        glCanvas.Bind(wx.EVT_MOUSE_EVENTS, self.onEvtMouse)

    def onEvtMouse(self, evt):
        etype, srcBtn = self.wxEtypeMap[evt.GetEventType()]
        eoHeight = evt.GetEventObject().GetClientSize()[1]

        info = dict(
            etype=etype,
            pos=(evt.m_x, eoHeight - evt.m_y), # change to bottom left orientation
            buttonSource=srcBtn,
            buttons=((evt.m_leftDown and 0x1) | (evt.m_rightDown and 0x2) | (evt.m_middleDown and 0x4)),
            modifers=((evt.m_altDown and 0x1) | (evt.m_controlDown and 0x2) | (evt.m_shiftDown and 0x4) | (evt.m_metaDown and 0x8)),
            timestamp=evt.GetTimestamp())

        if etype == 'wheel':
            info.update(
                wheel=evt.m_wheelRotation,
                wheelLinesPer=evt.m_linesPerAction,
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

