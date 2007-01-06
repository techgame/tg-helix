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
from TG.helix.events.viewportEvents import GLViewportEventHandler
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

class MatuiViewportEventHandler(GLViewportEventHandler):
    eventKinds = ['viewport']
    def __init__(self, scene):
        self.scene = scene

    def resize(self, glview, viewportSize):
        glview.setViewCurrent()
        return self.scene.performResize(glview, viewportSize)

    def erase(self, glview):
        return True

    def paint(self, glview):
        return self.scene.performRender(glview)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiInputEventHandler(MouseEventHandler, KeyboardEventHandler):
    eventKinds = ['mouse', 'keyboard']
    def __init__(self, scene):
        self.scene = scene

    def key(self, glview, info):
        glview.setViewCurrent()
        if info['etype'] in ('char',):
            print
            print 'Key Event:'
            pprint.pprint(info)
            return True
        else: return False

    def mouse(self, glview, info):
        glview.setViewCurrent()
        etype = info['etype']
        if etype in ('up', 'down', 'dclick'):
            print
            print 'Mouse Event:'
            pprint.pprint(info)

            if etype in ('down', 'dclick'):
                selection = self.scene.performSelect(glview, info['pos'])

                if selection:
                    pprint.pprint(selection)

            return True
        else: return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiTimingEventHandler(IdleEventHandler, TimerEventHandler):
    eventKinds = ['idle', 'timer']
    def __init__(self, scene):
        self.scene = scene

    def idle(self, glview, info):
        return False

    def timer(self, glview, info):
        self.scene.performAnimation(glview, info)
        return True

