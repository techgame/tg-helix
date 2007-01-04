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

from TG.observing import ObservableObjectWithProp, ObservableDict, ObservableList

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EventSource(object):
    """An event source demux captures events from the system and recategorizes
    them into event roots like mice, and keyboards.
    
    The general idea is that events that are captured will be categorized into
    event roots, and then forward to that host.  The events should also be
    normalized at this layer.
    """

    kind = None
    def iterHandlers(self, kind=None):
        if self.root is None:
            return iter(())
        if kind is None:
            kind = self.kind
        return self.root.iterHandlers(kind)

    _root = None
    def getRoot(self):
        return self._root
    def setRoot(self, root):
        self._root = root
    root = property(getRoot, setRoot)

    def accept(self, visitor):
        return visitor.visitEventSource(self, [self.kind])

class GLEventSource(EventSource):
    if sys.platform.startswith('win'):
        # time.clock is the fastest updating query on unix heritage platforms
        newTimestamp = staticmethod(time.clock)
    else:
        # time.time is the fastest updating query on windows
        newTimestamp = staticmethod(time.time)

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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Event Root to coordinate the EventSources with the event Handlers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EventRoot(ObservableObjectWithProp):
    """An event root is an object that represents an object that has events.
    Examples are mice, keyboards, joysticks.  These objects recreate state from
    the events they recieve from EventSource.
    """

    sources = ObservableDict.property()
    SourceList = ObservableList

    handlersByKind = ObservableDict.property()
    HandlerList = ObservableList

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
            evtSrc.setRoot(self)

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
            evth.setRoot(self)

            if evth not in handlers:
                handlers.append(evth)

