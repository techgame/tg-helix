# -*- coding: utf-8 -*- vim: set ts=4 sw=4 expandtab
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2012  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the MIT style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

import Cocoa
from .common import CocoaEventSourceMixin

def nsMapping(ns, suffix, fn=str.lower):
    for name, enum in vars(ns).iteritems():
        if name.endswith(suffix):
            name = name[len('NS'):-len(suffix)]
            yield enum, fn(name)

class CocoaKeyboardEventSource(CocoaEventSourceMixin):
    channelKey = 'key'

    def bindHost(self, glview, options):
        glview.events.bind('key', self.onEvtKey)

    def onEvtKey(self, evt, etype, ekind):
        keyCode = evt.keyCode()
        uchar = evt.characters()
        unikey = ord(uchar) if uchar else None
        token = self.cocoaTranslate.get(uchar, uchar)

        info = self.newInfo(etype=etype, ekind=ekind)
        info.update(ukey=unikey, uchar=uchar, token=token)
        if not self.addKeyMouseInfo(info, None, evt):
            return

        self.evtRoot.send(self.channelKey, info)

    cocoaTranslate = dict(nsMapping(Cocoa, 'FunctionKey'))
