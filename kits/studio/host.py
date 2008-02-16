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

from TG.skinning.toolkits.wx import wx, wxSkinModel, XMLSkin
from TG.kvObserving import KVObject, KVProperty

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xmlSkin = XMLSkin("""<?xml version='1.0'?>
<skin xmlns='TG.skinning.toolkits.wx'>
    <application />
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StudioHost(wxSkinModel, KVObject):
    xmlSkin = xmlSkin
    runSkin = False

    def __init__(self, mgr, appInfo, bSkinModel=True):
        KVObject.__init__(self)
        wxSkinModel.__init__(self)

        if bSkinModel:
            self.skinModel()

        self.setAppInfo(mgr, appInfo)

    def setAppInfo(self, mgr, appInfo):
        wxapp = wx.GetApp()
        if 'vendor' in appInfo:
            wxapp.SetVendorName(appInfo['vendor'])
        if 'appName' in appInfo:
            wxapp.SetAppName(appInfo['appName'])

    def exit(self):
        wxapp = wx.GetApp()
        wxapp.Exit()

