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

from loader import MatuiResourceLoader

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Resource Unit Definition
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiResourceSlot(object):
    def __init__(self, res, key):
        self.res = res
        self.key = key

    def get(self, *args):
        if args:
            return self.res.get(self.key, *args)
        else: return self.res[self.key]
    def set(self, value):
        self.res[self.key] = value
    def delete(self, value):
        del self.res[self.key]

    _loader = MatuiResourceLoader()
    def loader(self):
        return self._loader.forSlot(self)
    load = property(loader)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiResources(dict):
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, dict.__repr__(self))

    ResourceSlot = MatuiResourceSlot
    def slot(self, key):
        return self.ResourceSlot(self, key)

    _loader = MatuiResourceLoader()
    def loader(self, key=None):
        if key is None:
            return self._loader

        return self.slot(key).loader()
    load = property(loader)

