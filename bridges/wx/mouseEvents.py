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
        etype, btn = self.wxEtypeMap[evt.GetEventType()]
        info = self.newInfo(etype=etype, btn=btn, btnEvt='%s_%s'%(btn or '', etype))

        if etype == 'wheel':
            info.update(
                wheel=evt.GetWheelRotation(),
                wheelLinesPer=evt.GetLinesPerAction(),
                wheelIsPage=evt.IsPageScroll())

        kminfo = self.getKeyMouseInfo((evt.GetX(), evt.GetY()), evt)
        info.update(kminfo)

        self.channel.call_n2(self, info)
        if info.get('skip', False):
            evt.Skip()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    wxEtypeMap = {
        wx.wxEVT_ENTER_WINDOW: ('enter', None),
        wx.wxEVT_LEAVE_WINDOW: ('leave', None),

        wx.wxEVT_MOTION: ('motion', None),
        wx.wxEVT_MOUSEWHEEL: ('wheel', None),

        wx.wxEVT_LEFT_UP: ('up', 'left'),
        wx.wxEVT_LEFT_DOWN: ('down', 'left'),
        wx.wxEVT_LEFT_DCLICK: ('dclick', 'left'),

        wx.wxEVT_RIGHT_UP: ('up', 'right'),
        wx.wxEVT_RIGHT_DOWN: ('down', 'right'),
        wx.wxEVT_RIGHT_DCLICK: ('dclick', 'right'),

        wx.wxEVT_MIDDLE_UP: ('up', 'middle'),
        wx.wxEVT_MIDDLE_DOWN: ('down', 'middle'),
        wx.wxEVT_MIDDLE_DCLICK: ('dclick', 'middle'),
    }

