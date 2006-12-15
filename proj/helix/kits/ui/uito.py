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

from TG.observing import ObservableProperty

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIItemTypeObserver(ObservableTypeParticipant):
    def __init__(self, propMap):
        self.propMap = propMap

    def copy(self, propMapUpdate=()):
        self = self.__class__(self.propMap.copy())
        if propMapUpdate:
            self.propMap.update(propMapUpdate)
        return self

    def __copy__(self):
        return self.copy()

    def onObservableClassNew(self, selfAttrName, uiItemKlass, tcinfo):
        pass
    def onObservableClassInit(self, selfAttrName, uiItemKlass, tcinfo):
        kvars = tcinfo['kvars']
        propMap = self.propMap
        for n, v in kvars.items():
            pm = propMap.get(n, None)
            if pm is not None:
                setattr(uiItemKlass, n, pm(v))

    def onObservableInit(self, selfAttrName, uiItem):
        propMap = self.propMap
        for n, v in propMap.iteritems():
            iv = getattr(uiItem, n, None)

            if iv is None: iv = v()
            else: iv = iv.copy()

            setattr(uiItem, n, iv)

