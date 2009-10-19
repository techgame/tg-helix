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

from .common import wx, wxEventSourceMixin

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def nsMapping(ns, prefix, fn=str.lower):
    for name, enum in vars(ns).iteritems():
        if name.startswith(prefix):
            name = name[len(prefix):]
            yield enum, fn(name)

class wxKeyboardEventSource(wxEventSourceMixin):
    channelKey = 'key'

    def bindHost(self, glCanvas, options):
        glCanvas.Bind(wx.EVT_KEY_DOWN, self.onEvtKey)
        glCanvas.Bind(wx.EVT_KEY_UP, self.onEvtKey)
        glCanvas.Bind(wx.EVT_CHAR, self.onEvtKey)
        glCanvas.SetFocus()

    def onEvtKey(self, evt):
        etype, ekind = self.wxEtypeMap[evt.GetEventType()]

        unikey = evt.GetUnicodeKey()
        keyCode = evt.GetKeyCode()
        uchar = (unichr(unikey) if unikey else u'')
        token = self.wxkTranslate.get(keyCode, uchar)

        info = self.newInfo(etype=etype, ekind=ekind)
        info.update(ukey=unikey, uchar=uchar, token=token)
        if not self.addKeyMouseInfo(info, None, evt):
            evt.Skip()
            return

        self.evtRoot.send(self.channelKey, info)
        if info.get('skip', True):
            evt.Skip()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    wxEtypeMap = {
        wx.wxEVT_KEY_DOWN: ('key', 'down', ),
        wx.wxEVT_KEY_UP: ('key', 'up', ),
        wx.wxEVT_CHAR: ('key', 'char', ),
    }

    wxkTranslate = dict(nsMapping(wx, 'WXK_'))

