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

from TG.helix.events.eventSource import EventRoot
from TG.helix.events.viewportEvents import GLViewportEventHandler
from TG.helix.events.mouseEvents import MouseEventHandler
from TG.helix.events.keyboardEvents import KeyboardEventHandler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class KMEventHandler(MouseEventHandler, KeyboardEventHandler):
    eventKinds = ['mouse', 'keyboard']

    def key(self, glview, info):
        return True
        if info['etype'] == 'char':
            if info['token']:
                t = u'<%s>' % info['token']
            else: t = info['uchar']
            sys.stdout.write(t.encode("unicode_escape"))
            sys.stdout.flush()

    def mouse(self, glview, info):
        return True
        print info['pos'], info['buttons']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UISceneEventsMixin(object):
    evtRoot = EventRoot.property()
    def setupEvtSources(self, evtSources=[]):
        evtRoot = self.evtRoot
        evtRoot += evtSources

        evtRoot += GLViewportEventHandler(self)
        evtRoot += KMEventHandler()

