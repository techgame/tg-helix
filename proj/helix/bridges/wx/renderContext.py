#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import wx

from TG.helix.framework.renderContext import RenderContext

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class wxRenderContext(RenderContext):
    def __init__(self, glCanvas=None):
        if glCanvas is not None:
            self.setup(glCanvas)

    def setup(self, glCanvas):
        self._glCanvas = glCanvas
        self._captureRenderEvents()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _captureRenderEvents(self):
        self._glCanvas.Bind(wx.EVT_SIZE, self._onEvtSize)
        self._glCanvas.Bind(wx.EVT_ERASE_BACKGROUND, self._onEvtEraseBackground)
        self._glCanvas.Bind(wx.EVT_PAINT, self._onEvtPaint)

    def _onEvtSize(self, evt):
        self.sceneResize(tuple(evt.GetSize()))
    def _onEvtEraseBackground(self, evt):
        pass
    def _onEvtPaint(self, evt):
        if not self.sceneRefresh():
            evt.Skip()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getViewportSize(self):
        return tuple(self._glCanvas.GetClientSize())
    def setCurrent(self):
        return self._glCanvas.SetCurrent()
    def swapBuffers(self):
        return self._glCanvas.SwapBuffers()

