#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.geomath.data.kvBox import KVBox
from TG.openGL.raw import gl
from . import actor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewportResizeOp(actor.SGResizeOp):
    def init(self, node, actor): 
        self.box = actor.box
    def resize(self, sgo):
        box = self.box
        box.p1 = sgo.viewportSize
        gl.glViewport(*box.toflatlist())

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Viewport(actor.MatuiActor):
    _sgOps_ = {'resize': ViewportResizeOp}
    box = KVBox.property([0,0], [1,1], dtype='i')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ ClearViewport
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ClearViewportRenderOp(actor.SGRenderOp):
    mask = gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT
    def render(self, sgo):
        gl.glClear(self.mask)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ClearViewport(actor.MatuiActor):
    _sgOps_ = {'render': ClearViewportRenderOp}

