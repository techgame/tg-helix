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

from . import material
from . import mesh
from . import image
from . import font

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiResourceLoader(object):
    slot = None

    def __init__(self, master=None):
        if master is not None:
            self.__dict__.update(master.__dict__)

    def forSlot(self, slot):
        result = self.__class__(self)
        result.slot = slot
        return result

    def asResult(self, result):
        slot = self.slot
        if slot is not None:
            slot.set(result)
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def group(self, groupName):
        r = self._groups[groupName]
        return self.asResult(r)
    def addGroup(self, groupName, resources):
        self._groups[groupName] = resources

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def color(self, *args, **kw):
        pass

    def boxmesh(self, *args, **kw):
        r = mesh.BoxMesh(*args, **kw)
        return self.asResult(r)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def nullMaterial(self):
        r = material.NullMaterial()
        return self.asResult(r)

    def debugMaterial(self, *args, **kw):
        r = material.DebugMaterial(*args, **kw)
        return self.asResult(r)

