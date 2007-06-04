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
    mosaicSize = (1<<9, 1<<9)
    ts = TypeSetter(color = 'black', wrapMode='line')

    liSung = FTTypeface('/Library/Fonts/Apple LiSung Light.dfont', size)

    liSungVert = FTTypeface('/Library/Fonts/Apple LiSung Light.dfont', size)
    liSungVert._ftFace.allowVerticalLayout()

    helvetical = FTTypeface('/System/Library/Fonts/Helvetica.dfont', size)
    zapfino = FTTypeface('/Library/Fonts/Zapfino.dfont', size*3/4)
    normal = FTTypeface('/Library/Fonts/Times New Roman', size)
    italic = FTTypeface('/Library/Fonts/Times New Roman#italic', size)
    bold = FTTypeface('/Library/Fonts/Times New Roman#bold', size)
    funFont = FTTypeface('/Library/Fonts/MarkerFelt.dfont', size)

    ts.face = normal
    ts.color = 'black'
    print >> ts, 'A font',

    ts.face = bold
    ts.color = 'red'
    print >> ts, 'test',

    ts.face = italic
    ts.color = 'blue'
    print >> ts, 'of fun',
    ts.face = normal

    #ts.face = zapfino
    ts.color = 'green'
    print >> ts, 'proportions'
    ts.color = 'black'
    ts.face = normal

    print >> ts, 'Now, wasn\'t that',
    ts.face = funFont
    print >> ts, 'fun?'

    ts.face = liSung
    print >> ts, u'\u03a8\u03c8\u03b2'

    ts.face = liSung
    print >> ts, u'\u6a19\u6e96\u8a9e'

    ts.color = 'orange'
    ts.face = liSungVert
    print >> ts, u'\u6a19\u6e96\u8a9e'

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
    text.update(ts)
    
    layout.add(text).align(.5)

    if 0:
        pnlBox = Panel()
        pnlBox.box = text.box
        pnlBox.color = '#f:0:0:1'
        node += pnlBox

        pnlTextBox = Panel()
        pnlTextBox.box = text.textBox
        pnlTextBox.color = '#0:0:f:1'
        node += pnlTextBox

    #text.arena.pages[0].asImage(None, 'page_demoText.png')

    host = HelixHost(scene)
    host.show()
    host.run()


