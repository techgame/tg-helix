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

import os, sys
import weakref

from TG.metaObserving import OBFactoryMap
from TG.kvObserving import KVObject, KVProperty, KVDict

from .host import StudioHost
from .package import Package

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Studio Manager
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BaseDirector(KVObject):
    _fm_ = OBFactoryMap()
    mgr = KVProperty(None)

    def asWeakRef(self, cb=None):
        return weakref.ref(self, cb)
    def asWeakProxy(self, cb=None):
        return weakref.proxy(self, cb)

class BaseManager(KVObject):
    _fm_ = OBFactoryMap()
    director = KVProperty(None)

    def asWeakRef(self, cb=None):
        return weakref.ref(self, cb)
    def asWeakProxy(self, cb=None):
        return weakref.proxy(self, cb)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Studio 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StudioDirector(BaseDirector):
    def __init__(self, mgr):
        self.mgr = mgr

    def init(self):
        pass

class StudioManager(BaseManager):
    _fm_ = BaseManager._fm_.branch(
            StudioDirector = StudioDirector,
            StudioHost = StudioHost,
            StudioPackage = Package,
            )

    host = KVProperty(None)
    productions = KVProperty(KVDict)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, rootPkgName):
        self.package = self._fm_.StudioPackage(rootPkgName)
        self.director = self._fm_.StudioDirector(self)

    def init(self):
        if self.host is not None:
            return

        self.host = self._fm_.StudioHost(self)
        self.director.init()

    def run(self):
        self.host.run()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getProduction(self, key, orLoad=True):
        try:
            production = self.productions[key]
        except LookupError:
            if orLoad:
                production = self.loadProductionFor(key)
            else: production = None
        return production

    def loadProductionFor(self, key):
        prodModule = self.package.siteImport(key)
        return prodModule.loadProduction(self)

    def addProduction(self, key, production):
        self.productions[key] = production

