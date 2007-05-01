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

from TG.metaObserving import OBChannelSet

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EventHandler(object):
    """Event handlers are part of the Chain of Responsibility pattern.  They
    are links in that chain that may or may not handle the event.
    """
    evtRoot = None

    def evtRootSetup(self, evtRoot):
        self.evtRoot = evtRoot

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EventSource(object):
    """An event source demux captures events from the system and recategorizes
    them into event roots like mice, and keyboards.
    
    The general idea is that events that are captured will be categorized into
    event roots, and then forward to that host.  The events should also be
    normalized at this layer.
    """
    evtRoot = None

    def evtRootSetup(self, evtRoot):
        self.evtRoot = evtRoot

    def newTimestamp(self):
        return self.evtRoot.newTimestamp()

    def newInfo(self, **kw):
        kw.update(timestamp=self.newTimestamp())
        return kw

class HostViewEventSource(EventSource):
    def getViewSize(self):
        """getSize is provided by concrete implementations"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def setViewCurrent(self):
        """setCurrent is provided by concrete implementations"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def viewSwapBuffers(self):
        """viewSwapBuffers is provided by concrete implementations"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Event Root to coordinate the EventSources with the event Handlers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EventRoot(OBChannelSet):
    """An event root is an object that represents an object that has events.
    Examples are mice, keyboards, joysticks.  These objects recreate state from
    the events they recieve from EventSource.
    """

    def getChannels(self):
        return self

    def __iadd__(self, item):
        self.visit(item)
        return self

    def visit(self, item):
        evtRootSetup = getattr(item, 'evtRootSetup', None)
        if evtRootSetup is None:
            return self.visitGroup(item)

        return evtRootSetup(self)

    def visitGroup(self, itemGroup):
        for subItem in itemGroup:
            self.visit(subItem)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if sys.platform.startswith('win'):
        # time.clock is the fastest updating query on unix heritage platforms
        newTimestamp = staticmethod(time.clock)
    else:
        # time.time is the fastest updating query on windows
        newTimestamp = staticmethod(time.time)

