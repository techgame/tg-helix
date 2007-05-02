#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.kvObserving import KVObject
from TG.helix.actors.scene import HelixScene
from .node import MatuiNode

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiScene(HelixScene, KVObject):
    _fm_ = HelixScene._fm_.copy()
    _fm_.update(Node=MatuiNode)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setupEvtSources(self):
        evtRoot = self.evtRoot
        evtRoot.add('viewport-size', self.sg_resize)
        evtRoot.add('viewport-paint', self.sg_render)
        evtRoot.add('timer', self.sg_animate)

    def sg_resize(self, info=None):
        self.sgPass['load'](info)
        return self.sgPass['resize'](info)
    def sg_render(self, info=None):
        self.sgPass['load'](info)
        return self.sgPass['render'](info)
    def sg_select(self, info=None):
        self.sgPass['load'](info)
        return self.sgPass['select'](info)

    animate = False
    def sg_animate(self, info=None):
        if self.animate:
            return self.sg_render(info)

