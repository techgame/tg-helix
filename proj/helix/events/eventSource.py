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
    def iterHandlers(self):
        if self.root is None:
            return iter(())

        return self.root.iterHandlers(self.kind)

    _root = None
    def getRoot(self):
        return self._root
    def setRoot(self, root):
        self._root = root
    root = property(getRoot, setRoot)

    def acceptVisitor(self, visitor):
        return visitor.visitEventSource(self)

class GLEventSource(EventSource):
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

    def visit(self, item):
        item.acceptVisitor(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def visitEventSource(self, evtSrc):
        self.addSource(evtSrc)

    def addSource(self, evtSrc):
        kind = evtSrc.kind
        if kind not in self.handlersByKind:
            self.handlersByKind[kind] = self.HandlerList()
        evtSrc.setRoot(self)

        sources = self.sources.get(kind)
        if sources is None:
            sources = self.SourceList()
            self.sources[kind] = sources
        if evtSrc not in sources:
            sources.append(evtSrc)

    def addSourceGroup(self, evtSources):
        for evtSrc in evtSources:
            self.addSource(evtSrc)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def visitHandler(self, evth):
        self.addHandler(evth)

    def addHandler(self, evth):
        kind = evth.kind
        handlers = self.handlersByKind.get(kind)
        if handlers is None:
            handlers = self.HandlerList()
            self.handlersByKind[kind] = handlers

        if evth not in handlers:
            handlers.append(evth)

    def addHandlerGroup(self, evtHandlerGroup):
        for evth in evtHandlerGroup:
            self.addHandler(evth)

