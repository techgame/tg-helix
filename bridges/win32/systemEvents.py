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

from .common import Win32EventSourceMixin
from venster import windows

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

windows.WM_ACTIVATEAPP = WM_ACTIVATEAPP = 0x1c

class Win32SystemEventSource(Win32EventSourceMixin):
    channelKey = 'system'

    def bindHost(self, glwin, options):
        glwin.bindEvt(windows.WM_ACTIVATEAPP, self.onEvtActivate)
        glwin.bindEvt(windows.WM_ACTIVATE, self.onEvtActivate)

    def onEvtActivate(self, tgt, evt):
        etype, ekind, active = self.etypeMap[(evt.nMsg, bool(evt.wParam))]
        info = self.newInfo(etype=etype, ekind=ekind, active=active)
        if not self.addKeyMouseInfo(info): return
        self.evtRoot.send(self.channelKey, info)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    etypeMap = {
        (windows.WM_ACTIVATE, True): ('window', 'activate', True),
        (windows.WM_ACTIVATE, False): ('window', 'deactivate', False),

        (windows.WM_ACTIVATEAPP, True): ('app', 'activate', True),
        (windows.WM_ACTIVATEAPP, False): ('app', 'deactivate', False),
    }

