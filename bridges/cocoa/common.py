# -*- coding: utf-8 -*- vim: set ts=4 sw=4 expandtab
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2012  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

from itertools import combinations
from TG.helix.actors.events import EventSource
from Cocoa import NSEvent

def iterBitmap(values):
    v = [(1<<i, e) for i,e in enumerate(values)]
    yield 0, set()
    for i in xrange(0, len(values)):
        for comb in combinations(v,1+i):
            b = 0; e = set()
            for bi,ei in comb:
                b|=bi; e.add(ei)
            yield b, e

class CocoaEventSourceMixin(EventSource):
    def __init__(self, glview, options, theater):
        self.glview = glview
        self.evtRootSetup(theater.evtRoot)
        self.bindHost(glview, options)

    def __nonzero__(self):
        return bool(self.glview)

    def bindHost(self, glview, options):
        pass

    modifierMap = dict(iterBitmap(['shift', 'control', 'alt', 'meta']))
    buttonMap = dict(iterBitmap(['left', 'right', 'middle', 'button4', 'button5']))

    def addKeyMouseInfo(self, info, pos=None, evt=None):
        host = self.glview
        if not host: return None

        if pos is None:
            win = host.window()
            if win:
                pos = NSEvent.mouseLocation()
                pos = win.convertScreenToBase_(pos)
                pos = host.convertPoint_fromView_(pos, None)
                pos = tuple(pos)
            else: pos = (0,0)

        if evt is not None:
            modifiers = evt.modifierFlags()
        else: modifiers = NSEvent.modifierFlags()
        modifiers = self.modifierMap[(modifiers>>17) & 0xf]

        buttons = NSEvent.pressedMouseButtons()
        buttons = self.buttonMap[buttons&0x1f]

        info.update(pos=pos, modifiers=modifiers, buttons=buttons)
        return info

