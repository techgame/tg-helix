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

from functools import partial
from .units import MatuiLoaderMixin, MatuiMaterialUnit

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Loader Mixin
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MaterialLoaderMixin(MatuiLoaderMixin):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Material Resources
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiMaterial(MatuiMaterialUnit):
    partial = staticmethod(partial)

    cullStack = False
    def bind(self, actor, res, mgr):
        # Return a list of 0-parameter callables that only require mgr parameter
        return [self.partial(self.perform, actor, res, mgr)]

    def perform(self, actor, res, mgr):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def bindUnwind(self, actor, res, mgr):
        # Return a list of callables that only require mgr parameter
        # These get called on the stack return
        return []
        # By default, most materials do not need to do anything on unwind
        #return [self.partial(self.performUnwind, actor, res, mgr)]

    def performUnwind(self, actor, res, mgr):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DebugMaterial(MatuiMaterial):
    def __init__(self, name):
        self.name = name
    def perform(self, actor, res, mgr):
        print '%s(%s):' % (self.__class__.__name__, self.name)
        print '  - %r' % (actor,)
        print '  - res: %s' % (', '.join(res.keys()),)
MaterialLoaderMixin._addLoader_(DebugMaterial)

