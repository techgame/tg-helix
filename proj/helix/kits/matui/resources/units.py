##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiResourceUnit(object):
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
    def isResourceMaterial(self): 
        return True

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

