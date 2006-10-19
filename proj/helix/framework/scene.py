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

from .views import HelixView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixScene(HelixView):
    """A Helix scene is the root rendering object, which is simply a composite
    of all the actors below it.  It acts as a mediator, keeping links to event
    roots relevant to the scene.  
    
    It can also processes the different rendering modes to support picking, or
    picking through rendering colours.
    """

    def init(self):
        super(HelixScene, self).init()
        self.subviews = self.SubViewsFactory()

    def isHelixScene(self):
        return True

    def accept(self, visitor):
        return visitor.visitScene(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ctx = None
    def setup(self, ctx):
        self.ctx = ctx
        return True
    def shutdown(self, ctx):
        self.ctx = None
        return True
    def resize(self, ctx, size):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def refresh(self, ctx):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

