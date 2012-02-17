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

from .common import QtCore, QtGui, QE, qtEventSourceMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def nsMapping(ns, prefix, fn=str.lower):
    for name, enum in vars(ns).iteritems():
        if name.startswith(prefix):
            name = name[len(prefix):]
            yield enum, fn(name)

class qtKeyboardEventSource(qtEventSourceMixin):
    channelKey = 'key'
    _focusPolicy = QtCore.Qt.ClickFocus

    def bindHost(self, glHost, options):
        if self._focusPolicy is not None:
            glHost.setFocusPolicy(self._focusPolicy)

        glHost.bindEvent(QtGui.QKeyEvent, self.onEvtKey)

    def onEvtKey(self, evt):
        print "I have a key evt", evt
        etype, ekind = self.qtEtypeMap[evt.type()]
        if ekind is None:
            return

        uchar = unicode(evt.text())
        if uchar:
            unikey = ord(uchar)
        else: unikey = None
        keyCode = evt.key()
        token = self.qtkTranslate.get(keyCode, uchar)

        info = self.newInfo(etype=etype, ekind=ekind)
        info.update(ukey=unikey, uchar=uchar, token=token)
        if not self.addKeyMouseInfo(info, None, evt):
            return

        self.evtRoot.send(self.channelKey, info)
        if info.get('skip', False):
            return

        if uchar and ekind == 'down':
            info.ekind = ekind = 'char'
            if not (info.modifiers & self.qtCharSetFilter):
                self.evtRoot.send(self.channelKey, info)

        if info.get('handled', False):
            evt.accept()

        if not info.get('skip', False):
            evt.accept()

        return evt.isAccepted()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    qtCharSetFilter = set(['control', 'alt', 'meta'])
    qtEtypeMap = {
        QE.KeyPress: ('key', 'down'),
        QE.KeyRelease: ('key', 'up'),
        QE.ShortcutOverride: ('key', None),
    }

    qtkTranslate = dict(nsMapping(QtCore.Qt, 'Key_'))

