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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class EventHandler(object):
    """Event handlers are part of the Chain of Responsibility pattern.  They
    are links in that chain that may or may not handle the event.
    """
    eventKinds = []

    def accept(self, visitor):
        return visitor.visitEventHandler(self, self.eventKinds)

    _root = None
    def getRoot(self):
        return self._root
    def setRoot(self, root):
        self._root = root
    root = property(getRoot, setRoot)

class EventHandlingStrategy(EventHandler):
    """An instance of the composite and strategy patterns, this object decides
    how to forward events to other handlers.  
    
    A good example of this is figuring out where to send a mouse click in an
    OpenGL application.  When the click comes in from the mouse root, that
    strategy would ask the renderer to go through a pick operation with the
    proper coordinates to figure out which objects are under the cursor.  That
    filters the possible event handlers to the ones picked.  The strategy would
    then sort those and send the event to the topmost, down to the bottom until
    someone consumed the event.
    """

class EventHandlerFilter(EventHandler):
    """The handler filter's responsibility is to narrow a collection of filters
    down using some criterion.  In an opengl type framework, it would run the
    pick operation to figure out which objects are under the point in question.
    """

