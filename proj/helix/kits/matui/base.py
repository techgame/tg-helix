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
from TG.helix.framework.stage import HelixStage, HelixActor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiStage(HelixStage):
    viewVisitKeys = ["MatuiStage"]

    minSize = None
    maxSize = None
    box = Rect.property()

    def loadForScene(self, scene):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def isMatuiNode(self): return False
    def isMatuiActor(self): return False

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

