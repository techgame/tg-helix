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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StudioHostBase(object):
    def __init__(self, mgr, appInfo, bSkinModel=True):
        self.createApp(mgr)
        self.setAppInfo(mgr, appInfo)

    def createApp(self, mgr):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def setAppInfo(self, mgr, appInfo):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def run(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

    def exit(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

