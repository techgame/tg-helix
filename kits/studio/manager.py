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

from .director import StudioDirector
from .host import StudioHost

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Packages for Production Loading
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

module = type(sys)

class Package(module):
    def __init__(self, name=None, registry=True):
        module.__init__(self, name or self.__name__)
        self.__file__ = '<dynamic package>'
        self.__path__ = []

        if registry:
            self._register_(registry)

    def _register_(self, registry=True):
        if registry in (None, True):
            registry = sys.modules

        registry[self.__name__] = self

        parentName, _, pkgName = self.__name__.rpartition('.')
        if parentName:
            parent = registry[parentName]
            setattr(parent, pkgName, self)

    def addSite(self, path):
        path = os.path.abspath(path)
        self.__path__.append(path)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StudioPackage(Package):
    __name__ = 'Studio'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Studio Manager
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StudioManager(KVObject):
    _fm_ = OBFactoryMap(
            StudioDirector = StudioDirector,
            StudioHost = StudioHost,
            StudioPackage = StudioPackage,
            )

    director = KVProperty(None)
    host = KVProperty(None)

    def __init__(self):
        self.setup()

    def setup(self):
        self.director = self._fm_.StudioDirector(self)
        self.host = self._fm_.StudioHost(self)

        self.package = self._fm_.StudioPackage()

    def addPackageSite(self, site):
        self.package.addSite(site)

    def run(self):
        self.host.run()

