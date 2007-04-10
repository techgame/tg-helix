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

from .units import MatuiGroupUnit
from .loader import MatuiResourceLoader

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Resource Unit Definition
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

factory = MatuiResourceLoader()
class MatuiResourceSlot(object):
    def __init__(self, res, key=None):
        self.res = res
        self.key = key

    def loadResource(self, value):
        key = self.key
        if key is None:
            self.res.update(value)
        else:
            self.res[key] = value

    factory = factory
    def loader(self):
        return self.factory.forSlot(self)
    load = property(loader)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiResourceObject(object):
    def __init__(self, instdata):
        self.__dict__ = instdata

    def __getitem__(self, key):
        return self.__dict__.__getitem__(key)
    def __setitem__(self, key, value):
        return self.__dict__.__setitem__(key, value)
    def __delitem__(self, key):
        return self.__dict__.__delitem__(key)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiResources(MatuiGroupUnit, dict):
    def isResourceGroup(self):
        return True

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, dict.__repr__(self))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def copy(self):
        result = MatuiResources()
        result.update(self)
        return result
    def forActor(self, actor):
        return self.copy()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    factory = factory
    def __enter__(self):
        return (MatuiResourceObject(self), self.factory)
    def __exit__(self, exc_value=None, exc_type=None, exc_tb=None):
        pass

    ResourceSlot = MatuiResourceSlot
    def slot(self, key=None):
        return self.ResourceSlot(self, key).loader()

