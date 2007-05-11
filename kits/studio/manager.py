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
    mgr = KVProperty(None)

    def __init__(self, mgr):
        self.mgr = mgr

    def init(self):
        pass

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
        self.package = self._fm_.StudioPackage(rootPkgName)
        self.director = self._fm_.StudioDirector(self)

    def init(self):
        self.host = self._fm_.StudioHost(self)
        self.director.init()

    def run(self):
        self.host.run()

