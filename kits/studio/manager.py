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

from TG.kvObserving import KVObject, KVProperty, KVDict

from .director import StudioDirector
from .host import StudioHost
from .theater import TheaterStage

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class StudioManager(KVObject):
    StudioDirector = StudioDirector
    StudioHost = StudioHost
    TheaterStage = TheaterStage

    director = KVProperty(None)
    host = KVProperty(None)
    theaters = KVProperty(KVDict)

    def __init__(self):
        self.setup()

    def setup(self):
        self.director = self.StudioDirector(self)
        self.host = self.StudioHost(self)

    def run(self):
        self.host.run()

    def theater(self, key=None):
        t = self.theaters.get(key, None)
        if t is None:
            t = self.TheaterStage(self)
            self.theaters[key] = t
        return t

