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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiResourceUnit(object):
    partial = staticmethod(partial)

    def isResource(self): return True
    def isResourceGroup(self): return False
    def isResourceMaterial(self): return False

    def isResourceMesh(self): return False

    def isResourceTexture(self): return False
    def isResourceFont(self): return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiGroupUnit(MatuiResourceUnit):
    def isResourceGroup(self): 
        return True

class MatuiMaterialUnit(MatuiResourceUnit):
    # Setting cullStack to a true value will prevent nexted
    # materials from being rendered, and will proceed to the
    # next peer# Setting cullStack to a true value will
    # prevent nexted materials from being rendered, and will
    # proceed to the next peer
    cullStack = False 

    def isResourceMaterial(self): 
        return True

    def bind(self, actor, res, mgr):
        '''Returns a list of 0-parameter callables for a
        render pass using this material.'''
        return []

    def bindUnwind(self, actor, res, mgr):
        '''Returns a list of 0-parameter callables for a
        render unwind pass using this material.  

        Ex. pop stacks, compile results, etc.'''
        return []

class MatuiMeshUnit(MatuiResourceUnit):
    def isResourceMesh(self): 
        return True

class MatuiTextureUnit(MatuiResourceUnit):
    texture = None
    def isResourceTexture(self): 
        return True

class MatuiFontUnit(MatuiTextureUnit):
    def isResourceFont(self): 
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Loader Mixin
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiLoaderMixin(object):
    @classmethod
    def _addLoader_(klass, loader, name=None):
        if name is None: name = loader.__name__

        def wrapMethod(self, *args, **kw):
            r = loader(*args, **kw)
            return self.asResult(r)
        wrapMethod.__name__ = name

        setattr(klass, name, wrapMethod)
        return loader

