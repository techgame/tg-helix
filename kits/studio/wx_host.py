##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2007  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import wx
from .host import StudioHostBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxStudioHost(StudioHostBase):
    def createApp(self, mgr):
        self._app = wx.GetApp() or wx.PySimpleApp()
        return self._app

    def setAppInfo(self, mgr, appInfo):
        app = wx.GetApp()
        if 'vendor' in appInfo:
            app.SetVendorName(appInfo['vendor'])
        if 'appName' in appInfo:
            app.SetAppName(appInfo['appName'])

    def run(self):
        app = wx.GetApp()
        return app.MainLoop()

    def exit(self):
        app = wx.GetApp()
        app.Exit()

