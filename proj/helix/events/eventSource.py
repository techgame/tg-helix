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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EventHandler(object):
    """Event handlers are part of the Chain of Responsibility pattern.  They
    are links in that chain that may or may not handle the event.
    """
    eventKinds = []
    root = None

    def accept(self, visitor):
        return visitor.visitEventHandler(self, self.eventKinds)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EventSource(object):
    """An event source demux captures events from the system and recategorizes
    them into event roots like mice, and keyboards.
    
    The general idea is that events that are captured will be categorized into
    event roots, and then forward to that host.  The events should also be
    normalized at this layer.
    """

    root = None

    kind = None
    def iterHandlers(self, kind=None):
        if self.root is None:
            return iter(())
        if kind is None:
            kind = self.kind
        return self.root.iterHandlers(kind)

    def accept(self, visitor):
        return visitor.visitEventSource(self, [self.kind])

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

    def newInfo(self, **kw):
        kw.update(timestamp=self.newTimestamp())
        return kw

    def newTimestamp(self):
        return self.root.newTimestamp()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Event Root to coordinate the EventSources with the event Handlers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EventRoot(object):
    """An event root is an object that represents an object that has events.
    Examples are mice, keyboards, joysticks.  These objects recreate state from
    the events they recieve from EventSource.
    """

    sources = None
    SourcesDict = dict
    SourceList = list

    handlersByKind = None
    HandlersByKindDict = dict
    HandlerList = list

    def __init__(self):
        self.sources = self.SourcesDict()
        self.handlersByKind = self.HandlersByKindDict()

    def iterHandlers(self, kind):
        return iter(self.handlersByKind[kind])

    def __iadd__(self, item):
        self.visit(item)
        return self

    def visit(self, item):
        accept = getattr(item, 'accept', None)
        if accept is not None:
            return accept(self)

        else: return self.visitGroup(item)

    def visitGroup(self, itemGroup):
        for subItem in itemGroup:
            self.visit(subItem)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def visitEventSource(self, evtSrc, eventKinds):
        for kind in eventKinds:
            if kind not in self.handlersByKind:
                self.handlersByKind[kind] = self.HandlerList()
            evtSrc.root = self

            sources = self.sources.get(kind)
            if sources is None:
                sources = self.SourceList()
                self.sources[kind] = sources
            if evtSrc not in sources:
                sources.append(evtSrc)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def visitEventHandler(self, evth, eventKinds):
        for kind in eventKinds:
            handlers = self.handlersByKind.get(kind)
            if handlers is None:
                handlers = self.HandlerList()
                self.handlersByKind[kind] = handlers
            evth.root = self

            if evth not in handlers:
                handlers.append(evth)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if sys.platform.startswith('win'):
        # time.clock is the fastest updating query on unix heritage platforms
        newTimestamp = staticmethod(time.clock)
    else:
        # time.time is the fastest updating query on windows
        newTimestamp = staticmethod(time.time)

