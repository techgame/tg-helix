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

