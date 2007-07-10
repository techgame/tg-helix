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
from TG.geomath.typeset.typeface import FTFixedTypeface

from utils import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import pygments
from pygments.lexers import guess_lexer
from pygments.formatter import Formatter
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Token, Whitespace

FormatScheme = {
    Token:              ('black',       'regular'),

    Whitespace:         ('lightgray',   'regular'),
    Comment:            ('gray',        'regular'),
    Keyword:            ('darkblue',    'bold'),
    Keyword.Type:       ('teal',        'bold'),
    Operator.Word:      ('purple',      'regular'),
    Name.Builtin:       ('teal',        'regular'),
    Name.Function:      ('darkgreen',   'regular'),
    Name.Namespace:     ('teal',        'regular'),
    Name.Class:         ('darkgreen',   'bold'),
    Name.Exception:     ('teal',        'bold'),
    Name.Decorator:     ('darkgray',    'regular'),
    Name.Variable:      ('darkred',     'regular'),
    Name.Constant:      ('darkred',     'regular'),
    Name.Attribute:     ('teal',        'regular'),
    Name.Tag:           ('blue',        'regular'),
    String:             ('brown',       'regular'),
    Number:             ('darkblue',    'regular'),

    Generic.Deleted:    ('red',         'regular'),
    Generic.Inserted:   ('darkgreen',   'regular'),
    Generic.Heading:    ('purple',      'regular'),
    Generic.Subheading: ('purple',      'regular'),
    Generic.Error:      ('red',         'bold'),

    Error:              ('red',         'bold'),
}
class TSFormatter(Formatter):
    def __init__(self, **options):
        Formatter.__init__(self, **options)
        self.scheme = options.get('scheme', None) or FormatScheme

    def format(self, tokensource, outfile):
        enc = self.encoding
        for ttype, value in tokensource:
            if enc: value = value.encode(enc)
            scheme = self.scheme.get(ttype)
            while scheme is None:
                ttype = ttype[:-1]
                scheme = self.scheme.get(ttype)

            if value:
                outfile.color = scheme[0]
                outfile.face = outfile.faceSet[scheme[1]]
                outfile.write(value)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    size = 12
    fn = '/Library/Fonts/Andale Mono'
    #fn = '/Library/Fonts/Courier New'
    #fn = '/System/Library/Fonts/Courier.dfont'
    #fn = '/System/Library/Fonts/Monaco.dfont'

    faceSet = {
        'bold': FTFixedTypeface(fn+'#bold', size),
        'italic': FTFixedTypeface(fn+'#italic', size),
        'regular': FTFixedTypeface(fn+'#regular', size),
    }

    ts = TypeSetter(color='black', wrapMode='line', face=faceSet['regular'], faceSet=faceSet)

    code = open(__file__, 'rU').read()
    pygments.highlight(code, guess_lexer(code), TSFormatter(), ts)

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
    
    layout.add(text).fill(50)

    if 1:
        pnlBox = Panel()
        pnlBox.box = text.box
        pnlBox.color = '#0:1'
        node += pnlBox

    host = HelixHost(scene)
    host.show()
    host.run()

