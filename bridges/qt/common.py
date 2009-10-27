##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2009  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.helix.actors.events import EventSource
from TG.helix.bridges.qt.libqt import QtCore, QtGui

Qt = QtCore.Qt
QE = QtCore.QEvent
QCursor = QtGui.QCursor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtEventSourceMixin(EventSource):
    def __init__(self, glHost, options, theater):
        self.glHost = glHost
        self.evtRootSetup(theater.evtRoot)
        self.bindHost(glHost, options)

    def __nonzero__(self):
        return bool(self.glHost)

    def bindHost(self, glHost, options):
        pass

    def addKeyMouseInfo(self, info, pos=None, evt=None):
        qthost = self.glHost
        if not qthost:
            return None

        if not hasattr(evt, 'modifiers'):
            modifiers = QtGui.qApp.keyboardModifiers()
        else: modifiers = evt.modifiers()
        if not hasattr(evt, 'buttons'):
            buttons = QtGui.qApp.mouseButtons()
        else: buttons = evt.buttons()

        if pos is None:
            pos = qthost.mapFromGlobal(QCursor.pos())
            pos = (pos.x(), pos.y())

        pos = (pos[0], qthost.height() - pos[1])

        modifiers = set(v for k, v in self.qtModifierMask if k & modifiers)
        buttons = set(v for k, v in self.qtButtonMask if k & buttons)

        info.update(pos=pos, buttons=buttons, modifiers=modifiers)

        return info

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    qtButtonMask = [
        (Qt.NoButton, None),
        (Qt.LeftButton, 'left'),
        (Qt.RightButton, 'right'),
        (Qt.MidButton, 'middle'),
        (Qt.XButton1, 'btnx1'),
        (Qt.XButton2, 'btnx2'),
        ]
    qtButtonMap = dict(qtButtonMask)

    qtModifierMask = [
        (Qt.NoModifier, None),
        (Qt.ShiftModifier, 'shift'),
        (Qt.ControlModifier, 'control'),
        (Qt.AltModifier, 'alt'),
        (Qt.MetaModifier, 'meta'),
        (Qt.KeypadModifier, 'keypad'),
        ]
    qtModifierMap = dict(qtModifierMask)

