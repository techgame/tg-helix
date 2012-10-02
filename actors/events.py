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

import sys
import time
import weakref

from TG.metaObserving import OBChannelSet

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EventInfo(object):
    @classmethod
    def fromInfo(klass, info):
        self = klass()
        self.__dict__ = info
        return self

    def __repr__(self):
        return '<%s keys: %s>' % (
            self.__class__.__name__, 
            ', '.join(self.__dict__.keys()), )

    def update(self, *args, **kw):
        return self.__dict__.update(*args, **kw)

    def __iter__(self): return iter(self.__dict__)
    def keys(self): return self.__dict__.keys()
    def values(self): return self.__dict__.values()
    def items(self): return self.__dict__.items()
    def iterkeys(self): return self.__dict__.iterkeys()
    def itervalues(self): return self.__dict__.itervalues()
    def iteritems(self): return self.__dict__.iteritems()

    def __len__(self):
        return len(self.__dict__)
    def __contains__(self, key):
        return key in self.__dict__
    def get(self, key, default=None):
        return self.__dict__.get(key, default)
    def __getitem__(self, key):
        return self.__dict__[key]
    def __setitem__(self, key, value):
        self.__dict__[key] = value
    def __delitem__(self, key):
        del self.__dict__[key]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getScene(self):
        return self.evtRoot.scene
    scene = property(getScene)

    def getSceneRootNode(self):
        return self.scene.root
    rootNode = property(getSceneRootNode)

    def getSceneRenderManager(self):
        return self.scene.srm
    srm = property(getSceneRenderManager)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EventSource(object):
    """An event source demux captures events from the system and recategorizes
    them into event roots like mice, and keyboards.
    
    The general idea is that events that are captured will be categorized into
    event roots, and then forward to that host.  The events should also be
    normalized at this layer.
    """
    evtRoot = None
    EventInfo = EventInfo

    def evtRootSetup(self, evtRoot):
        self.evtRoot = evtRoot

    def newTimestamp(self):
        return self.evtRoot.newTimestamp()

    def newInfo(self, **info):
        einfo = self.EventInfo.fromInfo(info)
        self.evtRoot._addEventInfo(einfo)
        return einfo

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Event Root to coordinate the EventSources with the event Handlers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EventRoot(OBChannelSet):
    """An event root is an object that represents an object that has events.
    Examples are mice, keyboards, joysticks.  These objects recreate state from
    the events they recieve from EventSource.
    """
    if sys.platform.startswith('win'):
        # time.clock is the fastest updating query on unix heritage platforms
        newTimestamp = staticmethod(time.clock)
    else:
        # time.time is the fastest updating query on windows
        newTimestamp = staticmethod(time.time)

    def __init__(self, scene):
        OBChannelSet.__init__(self)
        self.scene = scene
        self._wpself = weakref.proxy(self)

    def _addEventInfo(self, evtkw):
        evtkw.update(timestamp=self.newTimestamp(), evtRoot=self._wpself)
        return evtkw

    def send(self, channelKey, info):
        info.channel = channelKey
        try: return self.call_n1(channelKey, info)
        except Exception:
            sys.excepthook(*sys.exc_info())

