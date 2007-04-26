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

from TG.metaObserving import OBFactoryMap
from TG.kvObserving import KVObject, KVProperty, KVDict

from .host import StudioHost
from .package import Package

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Studio Manager
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StudioDirector(KVObject):
    manager = KVProperty(None)

    def __init__(self, manager):
        self.manager = manager

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StudioManager(KVObject):
    _fm_ = OBFactoryMap(
            StudioDirector = StudioDirector,
            StudioHost = StudioHost,
            StudioPackage = Package,
            )

    director = KVProperty(None)
    host = KVProperty(None)
    productions = KVProperty(KVDict)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, rootPkgName):
        self.setup(rootPkgName)

    def setup(self, rootPkgName):
        self.host = self._fm_.StudioHost(self)
        self.director = self._fm_.StudioDirector(self)

        self.package = self._fm_.StudioPackage(rootPkgName)

    def run(self):
        self.host.run()

