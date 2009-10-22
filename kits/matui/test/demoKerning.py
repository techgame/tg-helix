#!/usr/bin/env python
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

from TG.geomath.typeset.mosaic import MosaicPageArena
from TG.geomath.typeset.typesetter import TypeSetter
from TG.geomath.typeset.typeface import FTTypeface

from TG.helix.bridges.wx.host import HelixHost
from utils import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    size = 64

    allKernedFonts = [
        #'/Library/Fonts/Arial.ttf',
        #'/Library/Fonts/Arial Black.ttf',
        #'/Library/Fonts/Arial Narrow.ttf',
        #'/Library/Fonts/Arial Rounded Bold.ttf',
        #'/Library/Fonts/Brush Script.ttf',
        #'/Library/Fonts/Impact.ttf',
        #'/Library/Fonts/MarkerFelt.dfont',
        #'/Library/Fonts/PlantagenetCherokee.ttf',
        #'/Library/Fonts/Snell Roundhand',
        '/Library/Fonts/Times New Roman.ttf',
        #'/Library/Fonts/Trebuchet MS.ttf',
        #'/Library/Fonts/Verdana.ttf'
        ]

    kernedFont = FTTypeface(allKernedFonts[-1], size)

    mosaicSize = (1<<10, 1<<10)

    ts = TypeSetter(kern=True, face=kernedFont)
    ts1 = TypeSetter(kern=False, face=kernedFont)
    
    ts.write('(', color='black')
    ts.write('nominal', color='blue')
    ts.write(' | ', color='black')
    ts.write('kerned', color='red')
    ts.write(')', color='black')

    ts.color = 'red'
    print >> ts, '\nAviation\nWar',

    ts1.color = 'blue'
    print >> ts1, '\nAviation\nWar',

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    scene = MatuiTheater()

    node = scene.root
    node += Viewport()

    screen = ScreenOrtho()
    node += screen

    layout = screen.cell.newLayout(node=node)
    layout.watchHostBox(screen)

    pnl = Panel()
    pnl.color = 'white'
    layout.add(pnl)

    text = Text()
    text.arena = MosaicPageArena(mosaicSize)
    text.update(ts)

    layout.add(text).align(0, (0, 1), (10, -10))

    text1 = Text()
    text1.arena = text.arena
    text1.update(ts1)
    layout.add(text1).align(0, (0, 1), (10, -10))

    host = HelixHost(scene)
    host.show()
    host.run()

