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
    _fm_.update(Node = MatuiNode)

    _sgPassTypes_ = [
        ('load', True),
        ('render', False),
        ('resize', False),
        ('select', False),
        ('animate', False),
        ]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setupEvtSources(self):
        evtRoot = self.evtRoot
        evtRoot.add('viewport-size', self.sg_resize)
        evtRoot.add('viewport-paint', self.sg_render)
        evtRoot.add('timer', self.sg_animate)

    def sg_resize(self, info={}):
        self.sg_pass('load', info)
        return self.sg_pass('resize', info)
    def sg_render(self, info={}):
        self.sg_pass('load', info)
        return self.sg_pass('render', info)
    def sg_select(self, info={}):
        self.sg_pass('load', info)
        return self.sg_pass('select', info)

    animate = False
    def sg_animate(self, info={}):
        if not self.animate: 
            return False

        self.sg_pass('load', info)
        self.sg_pass('animate', info)
        return self.sg_pass('render', info)

