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
from TG.geomath.typeset.textblock import TextBlock
from TG.geomath.typeset.typeface import FTTypeface

from utils import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ipsum = '''\
Vestibulum tortor. Integer fermentum mi vitae augue venenatis pharetra. Pellentesque nunc. Fusce elementum. In hac habitasse platea dictumst. Fusce massa quam, gravida et, malesuada et, pellentesque nec, ante. Suspendisse risus nibh, vulputate vulputate, varius quis, elementum nec, justo. Sed vitae ipsum sed libero pharetra congue. Aenean ultrices turpis quis turpis. Morbi mattis, ipsum ut mollis suscipit, massa urna pulvinar urna, sit amet posuere eros odio ut tortor. Nulla accumsan, massa nec scelerisque bibendum, sapien nibh placerat erat, ut scelerisque magna tortor id libero. Fusce lorem justo, dapibus vel, tincidunt id, viverra sit amet, sem. Mauris pharetra sapien scelerisque arcu. Proin nec ante pretium nibh suscipit volutpat. Nunc commodo, enim eu iaculis egestas, risus magna vulputate elit, vitae euismod nibh tellus quis odio. In tincidunt. Etiam porta, pede a cursus consectetuer, est lorem dignissim dolor, in vestibulum eros sapien nec eros. Integer quis risus ut dui volutpat dignissim. Praesent vitae velit ac justo vestibulum viverra.

Morbi justo tellus, vehicula non, aliquam at, varius vel, lacus. Mauris nec magna. Pellentesque libero. Vivamus quis sem. Vestibulum et arcu eget arcu condimentum dignissim. Etiam velit dui, sodales nec, rutrum vel, sagittis at, sem. Quisque lacinia. In hac habitasse platea dictumst. Vestibulum semper, erat et molestie congue, dolor dui dapibus dolor, ut viverra elit mi in odio. Fusce elit mauris, volutpat ut, faucibus scelerisque, commodo id, eros. Etiam vulputate nibh et tellus. Nulla quis pede. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nunc purus tortor, vestibulum quis, ornare sed, posuere eu, arcu. Etiam lobortis elit quis nunc. Donec ornare, libero et lobortis tristique, arcu dolor convallis turpis, id hendrerit pede orci vel augue. Nam a nibh. Aliquam vel lectus.

Fusce dui odio, vulputate quis, laoreet sit amet, ullamcorper et, tellus. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Suspendisse a lectus. Duis dolor quam, ullamcorper eget, auctor ac, condimentum vel, purus. Ut augue. Donec porttitor porta erat. Nulla vel ligula. Vivamus in quam eu est vehicula pellentesque. Nulla auctor, magna in elementum rutrum, erat ante semper lacus, id porttitor lectus nibh nec nulla. Quisque tincidunt. Cras non sapien sit amet eros bibendum convallis. Nunc magna quam, pellentesque nec, suscipit non, ornare id, augue. Donec at neque.

Sed ac ipsum sit amet pede ullamcorper varius. Quisque nec odio ut eros egestas tempus. Quisque eu metus. Aliquam erat volutpat. Pellentesque tincidunt convallis magna. Donec non nunc in nunc tempor nonummy. Nam ac urna eget velit ornare dictum. Nam eu ligula. Aliquam at odio a nisl convallis aliquam. Maecenas tempus suscipit libero. Nunc sollicitudin tincidunt tortor. Mauris sem augue, egestas eu, vulputate non, pulvinar ut, mi. Maecenas posuere nisi id diam. Aliquam ac nisl non ligula congue faucibus.

Nunc et magna. Aenean vel metus. Duis in tortor. Proin commodo orci in odio. Integer nibh eros, sollicitudin nonummy, condimentum et, venenatis ut, ipsum. Proin pede purus, eleifend a, interdum feugiat, ullamcorper non, est. Curabitur laoreet est a arcu. Integer ullamcorper pede non tortor. Vivamus mollis lacinia mauris. Pellentesque a nunc pharetra nisi pretium tristique. Duis nec felis. Quisque blandit scelerisque leo. Nam fermentum elementum elit. Donec mauris risus, imperdiet non, vulputate et, malesuada ac, dolor. Integer lectus augue, posuere vel, tincidunt ac, dignissim vel, turpis. Nulla facilisi.
'''

if __name__=='__main__':
    size = 64
    ts = TypeSetter(color='black', wrapMode='line', wrapSize=(800,0))

    if 0:
        # test the rendering from multiple mosaic pages
        ts.block = TextBlock(False, (2*size,2*size))

    liSung = FTTypeface('/Library/Fonts/Apple LiSung Light.dfont', size)

    liSungVert = FTTypeface('/Library/Fonts/Apple LiSung Light.dfont', size)
    #liSungVert._ftFace.allowVerticalLayout()

    helvetical = FTTypeface('/System/Library/Fonts/Helvetica.dfont', size)
    zapfino = FTTypeface('/Library/Fonts/Zapfino.dfont', size*3/4)
    normal = FTTypeface('/Library/Fonts/Times New Roman', size)
    normalText = FTTypeface('/Library/Fonts/Times New Roman', 16)
    italic = FTTypeface('/Library/Fonts/Times New Roman#italic', size)
    bold = FTTypeface('/Library/Fonts/Times New Roman#bold', size)
    funFont = FTTypeface('/Library/Fonts/MarkerFelt.dfont', size)

    ts.face = normal

    if 0:
        ts.face = zapfino
        ts.write('')

    elif 0:
        ts.face = zapfino
        ts.write('ABCDEFGHIJKLMNOPQRSTUVWXYZ\n')
        ts.write('abcdefghijklmnopqrstuvwxyz\n')

    elif 0:
        ts.face = normalText
        aligns = ['left', 0.25, 'center', 0.75, 'right']
        colors = ['red', 'green', 'blue', 'orange', 'black']
        for idx, line in enumerate(ipsum.split('\n')):
            ts.write(line+'\n', wrapMode='text', color=colors[(idx>>1)%len(colors)], align=aligns[(idx>>1)%len(aligns)])

    elif 1:
        ts.write('A font ', face=normal, color='black')
        ts.write('test ', face=bold, color='red')
        ts.write('of fun ', face=italic, color='blue')
        ts.write('proportions\n\n', face=normal, color='green')
        ts.align = 'right'
        ts.write('Now, wasn\'t that ', face=funFont, color='black')
        ts.write('fun?\n\n')

        ts.align = 'center'
        ts.write(u'\u03a8\u03c8\u03b2\n', face=liSung)
        ts.write(u'\u6a19\u6e96\u8a9e\n', color='purple')
        ts.write(u'\u6a19\u6e96\u8a9e\n', color='orange', face=liSungVert)
    else:
        ts.face = normal
        ts.color = 'black'
        print >> ts, 'A font',

        ts.face = bold
        ts.color = 'red'
        print >> ts, u'test',

        ts.attr(face=italic, color='blue')
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
    text.update(ts)
    
    layout.add(text).fill(inset=50)

    if 1:
        pnlBox = Panel()
        pnlBox.box = text.box
        pnlBox.color = '#f:0:0:2'
        node += pnlBox

    host = HelixHost(scene)
    host.show()
    ts.block.arena.save()
    host.run()


