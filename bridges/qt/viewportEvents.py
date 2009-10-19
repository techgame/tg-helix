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

import sys
import traceback

from .common import QtGui, qtEventSourceMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtViewportEventSource(qtEventSourceMixin):
    channelKey = 'viewport'

    def bindHost(self, glCanvas, options):
        glCanvas.dgViewport = self

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def initializeGL(self):
        info = self.newInfo()
        if not self.addKeyMouseInfo(info):
            return False

        self.evtRoot.send(self.channelKey + '-init', info)

    def resizeGL(self, w, h):
        info = self.newInfo(viewSize=(w, h))
        if not self.addKeyMouseInfo(info):
            return False

        self.evtRoot.send(self.channelKey + '-size', info)

    def paintGL(self):
        info = self.newInfo()
        if not self.addKeyMouseInfo(info):
            return False

        self.evtRoot.send(self.channelKey + '-paint', info)

