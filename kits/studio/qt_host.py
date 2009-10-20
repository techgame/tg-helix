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

QtCore = QtGui = None

if None in [QtCore, QtGui]:
    try:
        from PySide import QtCore, QtGui
        from PySide.QtCore import SIGNAL, SLOT
    except ImportError:
        pass

if None in [QtCore, QtGui]:
    try:
        from PyQt4 import QtCore, QtGui
        from PyQt4.QtCore import SIGNAL, SLOT
    except ImportError:
        pass

if None in [QtCore, QtGui]:
    raise ImportError("Unable to import PySide or PyQt4 for Qt GUI support")


import sys
from .host import StudioHostBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtStudioHost(StudioHostBase, QtCore.QObject):
    def __init__(self, mgr, appInfo):
        QtCore.QObject.__init__(self)
        StudioHostBase.__init__(self, mgr, appInfo)

    def createApp(self, mgr):
        self._app = QtGui.QApplication(sys.argv)
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

