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
    def forView(self, view):
        return self

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __enter__(self):
        return (self.obj, self.load)
    def __exit__(self, exc_value=None, exc_type=None, exc_tb=None):
        pass

    ResourceSlot = MatuiResourceSlot
    def slot(self, key):
        return self.ResourceSlot(self, key).loader()

    _loader = MatuiResourceLoader()
    def loader(self, key=None):
        if key is not None:
            return self.slot(key)
        else: return self._loader
    load = property(loader)

    @property
    def obj(self):
        return MatuiResourceObject(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def loadGroup(self, groupName):
        grp = self.load.group(groupName, self)
        return grp.loadOnto(self)
    def addToLoader(self, groupName):
        self.load.addGroup(groupName, self)
    def addToGroup(self, group):
        group.update(self)
        return self

