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

from PyQt4 import QtCore
from PyQt4 import QtGui
from .host import StudioHostBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtStudioHost(StudioHostBase):
    def createApp(self, mgr):
        self._app = QtGui.qApp or QtGui.QApplication(sys.argv)
        return self._app

    def setAppInfo(self, mgr, appInfo):
        app = QtGui.qApp
        if 'vendor' in appInfo:
            app.setOrganizationName(appInfo['vendor'])
        if 'vendorDomain' in appInfo:
            app.setOrganizationDomain(appInfo['vendorDomain'])
        if 'appName' in appInfo:
            app.setApplicationName(appInfo['appName'])
        if 'appVersion' in appInfo:
            app.setApplicationVersion(appInfo['appVersion'])

    def run(self):
        QtGui.qApp.exec_()

    def exit(self):
        QtGui.qApp.exit()

