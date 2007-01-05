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
        self.managers = scene.managers

    def resize(self, glview, viewportSize):
        glview.setViewCurrent()
        layoutMgr = self.managers['layout']
        layoutMgr.layout(viewportSize)
        return True

    def erase(self, glview):
        return True

    def paint(self, glview):
        glview.setViewCurrent()
        renderMgr = self.managers['render']
        glview.frameStart()
        if renderMgr.render():
            glview.frameEnd()
            glview.viewSwapBuffers()
            return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiInputEventHandler(MouseEventHandler, KeyboardEventHandler):
    eventKinds = ['mouse', 'keyboard']
    def __init__(self, scene):
        self.scene = scene
        self.managers = scene.managers

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
        if info['etype'] in ('up', 'down', 'dclick'):
            selectMgr = self.managers['select']
            print
            print 'Mouse Event:'
            pprint.pprint(info)
            selection = selectMgr.select(info['pos'])
            if selection:
                pprint.pprint(selection)

            return True
        else: return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiTimingEventHandler(IdleEventHandler, TimerEventHandler):
    eventKinds = ['idle', 'timer']
    def __init__(self, scene):
        self.scene = scene
        self.managers = scene.managers

    def idle(self, glview, info):
        glview.setViewCurrent()
        return False

    if 1:
        def timer(self, glview, info):
            glview.setViewCurrent()
            renderMgr = self.managers['render']
            glview.frameStart()
            if renderMgr.render():
                glview.frameEnd()
                glview.viewSwapBuffers()
                return True
            return True
    else:
        def timer(self, glview, info):
            return False

