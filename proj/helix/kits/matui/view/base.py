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

from TG.helix.framework.views import HelixView
from TG.helix.framework.viewFactory import HelixViewFactory

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

matuiViewFactory = HelixViewFactory()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Base View for the Matui Framework
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiView(HelixView):
    viewForKeys = ['MatuiActor']
    viewFactory = matuiViewFactory

    @classmethod
    def fromViewable(klass, viewable):
        view = getattr(viewable, '__matui_view', None)
        if view is None:
            view = klass()
            setattr(viewable, '__matui_view', view)
            view.init(viewable)

        view.update(viewable)
        return view

    def __repr__(self):
        return '%s: %r' % (self.__class__.__name__, self.actor)

    actor = None
    def init(self, actor):
        self.actor = actor

    def update(self, actor):
        self.updateResources(actor.resources.forView(self))

    def updateResources(self, resources):
        render = resources.get('mat_render', None)
        if render is None:
            raise KeyError("%r cannot find a mat_render resource in %r" % (self, resources.keys()))
        self.sgRender = render.bind(self, resources)

        select = resources.get('mat_select', None)
        if select is None:
            raise KeyError("%r cannot find a mat_select resource in %r" % (self, resources.keys()))
        self.sgSelect = select.bind(self, resources)

