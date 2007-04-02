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

from .material import MaterialLoaderMixin
from .import stageMaterial 
from .mesh import MeshLoaderMixin
from .image import ImageLoaderMixin
from .font import FontLoaderMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiResourceLoader(
        MaterialLoaderMixin,
        MeshLoaderMixin,
        ImageLoaderMixin,
        FontLoaderMixin,
        ):

    def __init__(self, master=None):
        if master is not None:
            self.__dict__.update(master.__dict__)

    slot = None
    def forSlot(self, slot):
        result = self.__class__(self)
        result.slot = slot
        return result

    def asResult(self, result):
        slot = self.slot
        if slot is not None:
            slot.loadResource(result)
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

