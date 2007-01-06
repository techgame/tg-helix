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
from .units import MatuiMaterialUnit

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Rendering Resources
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiMaterial(MatuiMaterialUnit):
    def __call__(self, view, res, sgmgr):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def bind(self, view, res):
        return partial(self.__call__, view, res)

Material = MatuiMaterial

class NullMaterial(MatuiMaterial):
    def __call__(self, view, res, sgmgr):
        pass

class DebugMaterial(MatuiMaterial):
    def __init__(self, name):
        self.name = name
    def __call__(self, view, res, sgmgr):
        print '%s(%s):' % (self.__class__.__name__, self.name)
        print '  - %r' % (view,)
        print '  - res: %s' % (', '.join(res.keys()),)

