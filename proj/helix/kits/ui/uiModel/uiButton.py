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

from TG.observing import ObservableDict
from .uiBase import UIItem, UIItemWithBox, glData, numpy
from .uiWidgets import UIWidget, UIImage

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Button
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIButton(UIWidget):
    viewVisitKeys = ["UIButton"]

    stateMap = ObservableDict.property()
    def addState(self, stateKey, stateui):
        if not isinstance(stateui, UIItem):
            stateui = UIImage.fromItem(stateui)

        self.stateMap[stateKey] = stateui
        if self.state is None:
            self.state = stateKey

    stateui = None
    _state = None
    def getState(self):
        return self._state
    def setState(self, state):
        self.stateui = self.stateMap[state]
        self._state = state
    state = property(getState, setState)

