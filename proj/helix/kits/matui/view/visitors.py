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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Base Matui Visitor
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiVisitor(object):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Resize Visitor
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiResizeVisitor(MatuiVisitor):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Rendering Visitor
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiRenderVisitor(MatuiVisitor):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Selection Visitor
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiNameSelector(NameSelector):
    def __init__(self, info, pos, *args, **kw):
        self.info = info
        pos = Vector(pos+(0.,))
        NameSelector.__init__(self, pos, *args, **kw)

    def renderProjection(self, vpbox):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        self.renderPickMatrix(vpbox)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def _processHits(self, hitRecords, namedItems):
        selection = NameSelector._processHits(self, hitRecords, namedItems)
        selection.sort()
        return [s[-1] for s in selection]

class MatuiSelectionVisitor(MatuiVisitor):
    MatuiSelectorFactory = MatuiNameSelector

    def pick(self, pos, info):
        selector = self.MatuiSelectorFactory(info, pos)

        with selector:
            self.renderPick(selector)
            for view in self.views:
                view.renderPick(selector)
        return selector.selection

