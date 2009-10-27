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

from .common import QtCore, QtGui, QE, qtEventSourceMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtSystemEventSource(qtEventSourceMixin):
    channelKey = 'system'

    def bindHost(self, glHost, options):
        for qtype in self.qtEtypeMap.iterkeys():
            glHost.bindEvent(qtype, self.onEvtActivate)

    def onEvtActivate(self, evt):
        etype, ekind, active = self.qtEtypeMap[evt.type()]
        info = self.newInfo(etype=etype, ekind=ekind, active=active)

        if not self.addKeyMouseInfo(info):
            return

        self.evtRoot.send(self.channelKey, info)
        if not info.get('skip', False):
            evt.accept()
            return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    qtEtypeMap = {
        QE.WindowActivate: ('window', 'activate', True),
        QE.WindowDeactivate: ('window', 'deactivate', False),

        QE.ApplicationActivate: ('app', 'activate', True),
        QE.ApplicationDeactivate: ('app', 'deactivate', False),
    }

