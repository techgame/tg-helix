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
    _fm_.update(Node = MatuiNode,)

    _sgPassTypes_ = [
        ('load', True),
        #('pre-render', False),
        ('render', False),

        ('resize', False),

        #('pre-select', False),
        ('select', False),

        ('animate', False),
        ]

    _sgPassTriggers_ = [
        ('render', ['load', 'pre-render'], []),
        ('resize', ['load'], []),
        ('select', ['load', 'pre-select'], []),
        ('animate', ['load'], []),
        ]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setupEvtSources(self):
        evtRoot = self.evtRoot
        evtRoot.add('viewport-size', self.sg_resize)
        evtRoot.add('viewport-paint', self.sg_render)
        evtRoot.add('timer', self.sg_animate)

    def sg_resize(self, info=None):
        return self.sg_pass('resize', info)
    def sg_render(self, info=None):
        return self.sg_pass('render', info)
    def sg_select(self, info=None):
        return self.sg_pass('select', info)
    def sg_load(self):
        return self.sg_pass('load')

    animate = False
    def sg_animate(self, info=None):
        if self.animate: 
            self.sg_pass('animate', info)

        if self.srm.invalidated:
            return self.sg_render(info)

