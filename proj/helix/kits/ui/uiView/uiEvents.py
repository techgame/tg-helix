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

from __future__ import with_statement

import sys
import pprint

from TG.openGL.data import Vector
from TG.openGL.selection import NameSelector
from TG.openGL.raw import gl

from TG.helix.events.eventSource import EventRoot
from TG.helix.events.viewportEvents import GLViewportEventHandler
from TG.helix.events.mouseEvents import MouseEventHandler
from TG.helix.events.keyboardEvents import KeyboardEventHandler
from TG.helix.events.timerEvents import IdleEventHandler, TimerEventHandler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class KMEventHandler(MouseEventHandler, KeyboardEventHandler, IdleEventHandler, TimerEventHandler):
    eventKinds = ['mouse', 'keyboard', 'idle', 'timer']

    def __init__(self, scene):
        super(KMEventHandler, self).__init__()
        self.scene = scene

    def key(self, glview, info):
        glview.setViewCurrent()
        return True

    def mouse(self, glview, info):
        glview.setViewCurrent()
        if info['etype'] in ('up', 'down', 'dclick'):
            selection = self.scene.pick(info['pos'], info)
            print
            pprint.pprint(info)
            pprint.pprint(selection)
        return True

    def idle(self, glview, info):
        glview.setViewCurrent()
        return False

    def timer(self, glview, info):
        glview.setViewCurrent()
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UINameSelector(NameSelector):
    def __init__(self, info, pos, *args, **kw):
        self.info = info
        pos = Vector(pos+(0.,))
        NameSelector.__init__(self, pos, *args, **kw)

    def renderProjection(self, vpbox):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        self.renderPickMatrix(vpbox)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def _processHits(self, hitRecords, namedItems):
        selection = NameSelector._processHits(self, hitRecords, namedItems)
        selection.sort()
        return [s[-1] for s in selection]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UISceneEventsMixin(object):
    evtRoot = EventRoot.property()

    UISelectorFactory = UINameSelector
    def setupEvtSources(self, evtSources=[]):
        evtRoot = self.evtRoot
        evtRoot += evtSources

        evtRoot += GLViewportEventHandler(self)
        evtRoot += KMEventHandler(self)

    def pick(self, pos, info):
        selector = self.UISelectorFactory(info, pos)

        with selector:
            self.renderPick(selector)
            for view in self.views:
                view.renderPick(selector)
        return selector.selection

