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

import numpy
from TG.openGL import data as glData
from TG.openGL.data import Rect

from TG.helix.framework.stage import HelixActor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiStage(HelixActor):
    viewVisitKeys = ["MatuiStage"]

    box = Rect.property()
    minSize = None
    maxSize = None

    def isMatuiNode(self): return False
    def isMatuiActor(self): return False

    def isHelixStage(self):
        return True
    def accept(self, visitor):
        return visitor.visitStage(self)

    def loadForScene(self, scene):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiActor(HelixActor):
    viewVisitKeys = ['MatuiActor']

    box = Rect.property()
    minSize = None
    maxSize = None

    def isMatuiNode(self): return False
    def isMatuiActor(self): return True

    def onCellLayout(self, cell, cbox):
        self.box.copyFrom(cbox)

