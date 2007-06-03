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

    zapfino = FTTypeface('/Library/Fonts/Zapfino.dfont', size*3/4)
    chalkboard = FTTypeface('/Library/Fonts/Chalkboard.ttf', size)
    chalkboardBold = FTTypeface('/Library/Fonts/ChalkboardBold.ttf', size)

    mosaicSize = (1<<10, 1<<10)

    ts = TypeSetter(color = 'black')
    
    ts.face = chalkboard
    ts.color = 'black'
    print >> ts, 'a font',

    ts.color = 'red'
    print >> ts, 'test',

    ts.color = 'blue'
    ts.face = zapfino
    print >> ts, 'of fun',

    ts.face = chalkboardBold
    ts.color = 'green'
    print >> ts, 'proportions',
    ts.color = 'black'

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

    layout.add(text).align(.5, .5, (0, size))

    host = HelixHost(scene)
    host.show()
    host.run()

