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

from .host import StudioHostBase
from .package import Package

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Studio Manager
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BaseManager(KVObject):
    _fm_ = OBFactoryMap()

    def asWeakRef(self, cb=None):
        return weakref.ref(self, cb)
    def asWeakProxy(self, cb=None):
        return weakref.proxy(self, cb)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Studio 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StudioManager(BaseManager):
    _fm_ = BaseManager._fm_.branch(
            StudioHost = StudioHostBase,
            StudioPackage = Package,

            hostAppInfo = {
                'vendor': 'TechGame Networks',
                'appName': 'Helix Studio Application'}
            )

    host = None
    productions = KVProperty(KVDict)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, rootPkgName):
        self.package = self._fm_.StudioPackage(rootPkgName)

    def init(self):
        if self.host is not None:
            return

        self._createHost()

    def _createHost(self):
        Factory = self._fm_.StudioHost
        if Factory is not None:
            host = Factory(self, self._fm_.hostAppInfo)
        else: host = None
        self.host = host

    def run(self):
        self.host.run()
    def exit(self):
        self.host.exit()

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
        return self.loadProduction(prodModule)

    def loadProduction(self, prodModule):
        return prodModule.loadProduction(self)

    def addProduction(self, key, production):
        self.productions[key] = production

