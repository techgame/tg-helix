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

class wxSystemEventSource(wxEventSourceMixin):
    channelKey = 'system'

    def bindHost(self, glCanvas, options):
        wxapp = wx.GetApp()
        wxapp.Bind(wx.EVT_ACTIVATE_APP, self.onEvtActivate)

        wxframe = glCanvas.GetTopLevelParent()
        wxframe.Bind(wx.EVT_ACTIVATE, self.onEvtActivate)

    def onEvtActivate(self, evt):
        etype, ekind, active = self.wxEtypeMap[evt.GetEventType(), bool(evt.GetActive())]
        info = self.newInfo(etype=etype, ekind=ekind, active=active)

        self.addKeyMouseInfo(info)

        self.evtRoot.send(self.channelKey, info)
        if info.get('skip', False):
            evt.Skip()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    wxEtypeMap = {
        (wx.wxEVT_ACTIVATE, True): ('window', 'activate', True),
        (wx.wxEVT_ACTIVATE, False): ('window', 'deactivate', False),

        (wx.wxEVT_ACTIVATE_APP, True): ('app', 'activate', True),
        (wx.wxEVT_ACTIVATE_APP, False): ('app', 'deactivate', False),
    }

