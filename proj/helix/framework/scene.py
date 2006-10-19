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

from TG.observing import ObservableObject, Observable, notifier

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixScene(Observable):
    """A Helix scene is the root rendering object, which is simply a composite
    of all the actors below it.  It acts as a mediator, keeping links to event
    roots relevant to the scene.  
    
    It can also processes the different rendering modes to support picking, or
    picking through rendering colours.
    """

    ctx = None

    def __init__(self):
        Observable.__init__(self)
        self.init()

    @notifier
    def init(self):
        pass

    @notifier
    def setup(self, renderContext):
        self.ctx = renderContext
        self.load()
        return True
    @notifier
    def load(self): 
        pass

    @notifier
    def shutdown(self, renderContext):
        self.ctx = renderContext
        self.unload()
        return True
    @notifier
    def unload(self): 
        pass

    @notifier
    def resize(self, renderContext, size):
        self.ctx = renderContext
        return True
    @notifier
    def refresh(self, renderContext):
        self.ctx = renderContext
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def accept(self, visitor):
        return visitor.visitScene(self)

    def acceptOnItems(self, visitor):
        self.views.accept(visitor)

