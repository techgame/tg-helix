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

import pprint

from TG.helix.events.eventSource import EventRoot
from TG.helix.events.viewportEvents import ViewportEventHandler
from TG.helix.events.mouseEvents import MouseEventHandler
from TG.helix.events.keyboardEvents import KeyboardEventHandler
from TG.helix.events.timerEvents import IdleEventHandler, TimerEventHandler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiEventRoot(EventRoot):
    def configFor(self, scene, evtSources):
        self += evtSources

        self += MatuiViewportEventHandler(scene)
        self += MatuiInputEventHandler(scene)
        self += MatuiTimingEventHandler(scene)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiViewportEventHandler(ViewportEventHandler):
    eventKinds = ['viewport']
    def __init__(self, scene):
        self.scene = scene

    def resize(self, hostView, viewportSize):
        return self.scene.performResize(hostView, viewportSize)

    def erase(self, hostView):
        return True

    def paint(self, hostView):
        return self.scene.performRender(hostView)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiInputEventHandler(MouseEventHandler, KeyboardEventHandler):
    eventKinds = ['mouse', 'keyboard']
    def __init__(self, scene):
        self.scene = scene

    def key(self, hostView, info):
        hostView.setViewCurrent()
        if info['etype'] in ('char',):
            print
            print 'Key Event:'
            pprint.pprint(info)
            return True
        else: return False

    def mouse(self, hostView, info):
        hostView.setViewCurrent()
        etype = info['etype']
        if etype in ('up', 'down', 'dclick'):
            print
            print 'Mouse Event:'
            pprint.pprint(info)

            if etype in ('down', 'dclick'):
                selection = self.scene.performSelect(hostView, info['pos'])

                if selection:
                    pprint.pprint(selection)

            return True
        else: return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiTimingEventHandler(IdleEventHandler, TimerEventHandler):
    eventKinds = ['idle', 'timer']
    def __init__(self, scene):
        self.scene = scene

    def idle(self, hostView, info):
        return False

    def timer(self, hostView, info):
        self.scene.performAnimation(hostView, info)
        return True

