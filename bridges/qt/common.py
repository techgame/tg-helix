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

QtCore = QtGui = None

if None in [QtCore, QtGui]:
    try:
        from PySide import QtCore, QtGui
        from PySide.QtCore import SIGNAL, SLOT
    except ImportError:
        pass

if None in [QtCore, QtGui]:
    try:
        from PyQt4 import QtCore, QtGui
        from PyQt4.QtCore import SIGNAL, SLOT
    except ImportError:
        pass

if None in [QtCore, QtGui]:
    raise ImportError("Unable to import PySide or PyQt4 for Qt GUI support")

from TG.helix.actors.events import EventSource

Qt = QtCore.Qt
QE = QtCore.QEvent
QCursor = QtGui.QCursor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtEventSourceMixin(EventSource):
    def __init__(self, glCanvas, options, theater):
        self.glCanvas = glCanvas
        self.evtRootSetup(theater.evtRoot)
        self.bindHost(glCanvas, options)

    def __nonzero__(self):
        return bool(self.glCanvas)

    def bindHost(self, glCanvas, options):
        pass

    def addKeyMouseInfo(self, info, pos=None, evt=None):
        qthost = self.glCanvas
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

        modifiers = [v for k, v in self.qtModifierMask if k & modifiers]
        buttons = [v for k, v in self.qtButtonMask if k & buttons]

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

