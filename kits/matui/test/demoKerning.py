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

from utils import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    size = 64

    allKernedFonts = [
        #'/Library/Fonts/Arial',
        #'/Library/Fonts/Arial Black',
        #'/Library/Fonts/Arial Narrow',
        #'/Library/Fonts/Arial Rounded Bold',
        #'/Library/Fonts/Brush Script',
        #'/Library/Fonts/Impact',
        #'/Library/Fonts/MarkerFelt.dfont',
        #'/Library/Fonts/PlantagenetCherokee.ttf',
        #'/Library/Fonts/Snell Roundhand',
        '/Library/Fonts/Times New Roman',
        #'/Library/Fonts/Trebuchet MS',
        #'/Library/Fonts/Verdana'
        ]

    kernedFont = FTTypeface(allKernedFonts[-1], size)

    mosaicSize = (1<<10, 1<<10)

    ts = TypeSetter(color = 'black')
    ts1 = TypeSetter(color = 'black', kern=False)
    
    ts.face = kernedFont
    print >> ts, 'War of Aviation (kerned)',

    ts1.face = kernedFont
    print >> ts1, 'War of Aviation (not kerned)',

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    scene = MatuiScene()

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
    text.sorts = ts.sorts

    layout.add(text).align(0, (0, 1), (10, -10 - size))

    text1 = Text()
    text1.arena = text.arena
    text1.sorts = ts1.sorts
    layout.add(text1).align(0, (0, 1), (10, -10 - 2*size))

    host = HelixHost(scene)
    host.show()
    host.run()

