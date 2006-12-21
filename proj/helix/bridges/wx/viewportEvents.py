#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from .common import wx, wxEventSourceMixin
from ..viewportEvents import GLViewportEventSource

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxGLViewportEventSource(wxEventSourceMixin, GLViewportEventSource):
    def __init__(self, glCanvas):
        GLViewportEventSource.__init__(self)
        wxEventSourceMixin.__init__(self, glCanvas)
        glCanvas.Bind(wx.EVT_SIZE, self.onEvtSize)
        glCanvas.Bind(wx.EVT_ERASE_BACKGROUND, self.onEvtEraseBackground)
        glCanvas.Bind(wx.EVT_PAINT, self.onEvtPaint)
        glCanvas.SetCurrent()

    def onEvtSize(self, evt):
        if not self.sendSize(tuple(evt.GetSize())):
            evt.Skip()

    def onEvtEraseBackground(self, evt):
        if not self.sendErase():
            evt.Skip()

    def onEvtPaint(self, evt):
        if not self.sendPaint():
            evt.Skip()

