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

from itertools import izip, starmap
from TG.openGL.raw.gl import *

from .scene import UIView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class WidgetView(UIView):
    viewForKeys = ['Widget']

    def init(self, widget):
        print self, widget
    def render(self, widget):
        self.renderBounds(widget.bounds, widget.color)

    def renderBounds(self, bounds, color=None):
        rect = bounds.box.vRect()
        if color is not None:
            glColor4f(*color)

        glBegin(GL_QUADS)
        for p in rect:
            glVertex3f(*p)
        glEnd()

    def renderItems(self, views, items=None):
        if items is None:
            for v in views:
                v.render(None)
        else:
            for v, i in izip(views, items):
                v.render(i)

