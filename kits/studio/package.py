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

