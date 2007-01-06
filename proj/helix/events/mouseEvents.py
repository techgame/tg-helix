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

from .eventSource import EventHandler, HostViewEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MouseEventSource(HostViewEventSource):
    kind = 'mouse'

    def sendMouse(self, info):
        for eh in self.iterHandlers():
            r = eh.mouse(self, info)
            if r is not None:
                return r

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MouseEventHandler(EventHandler):
    eventKinds = ['mouse']

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

    def mouse(self, hostview, info):
        pass

