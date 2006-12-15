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

from .uiViewBase import UIView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Widget Views
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class WidgetView(UIView):
    viewForKeys = ['Widget']

    partsByName = ['color', 'box']
    def init(self, widget):
        UIView.init(self, widget)
        self.update(widget)

    def _onViewableChange(self, viewable, attr, info=None):
        UIView._onViewableChange(self, viewable, attr, info=None)

        if attr in self.partsByName:
            self.update(viewable, [attr])

    def update(self, widget, partNames=None):
        if partNames is None:
            partNames = self.partsByName

        for name in partNames:
            part = getattr(widget, name)
            partView = self.viewFactory(part)
            setattr(self, name, partView)

    def render(self):
        UIView.render(self)
        for attr in self.partsByName:
            getattr(self, attr).render()

