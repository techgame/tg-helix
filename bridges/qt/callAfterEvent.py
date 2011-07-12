# -*- coding: utf-8 -*- vim: set ts=4 sw=4 expandtab:
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2011  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys
from functools import partial
from .libqt import QtCore, QtGui

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class qtCallAfterEvent(QtCore.QEvent):
    typeId = QtCore.QEvent.registerEventType()
    if hasattr(QtCore.QEvent, 'Type'):
        typeId = QtCore.QEvent.Type(typeId)

    def __init__(self):
        QtCore.QEvent.__init__(self, self.typeId)
    fn = None
    def bind(self, fn, *args, **kw):
        return self.bindEx(fn, args, kw)
    def bindEx(self, fn, args=None, kw=None):
        if args or kw:
            fn = partial(fn, *args, **kw)
        self.fn = fn 
        return self

    def perform(self):
        try: self.fn()
        except Exception:
            sys.excepthook(*sys.exc_info())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class QtCallAfterApi(object):
    def customEvent(self, evt):
        evt.perform()

    def callAfter(self, fn, *args, **kw):
        self.callAfterEx(fn, args, kw)
    def callAfterEx(self, fn, args=None, kw=None):
        evt = qtCallAfterEvent()
        evt.bindEx(fn, args, kw)
        QtGui.qApp.postEvent(self, evt)

