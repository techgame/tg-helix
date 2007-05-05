#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.kvObserving import KVObject
from TG.helix.actors.scene import HelixScene
from TG.helix.actors.sceneGraphPass import SceneGraphPass
from .node import MatuiNode

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiSceneGraphPass(SceneGraphPass):
    def sgBindOp(self, hostNode, opKey):
        hostNode.bindPass.add(opKey, self._sgBindPass_)

    def _sgBindPass_(self, node, ct):
        ct.add(self.perform)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiScene(HelixScene, KVObject):
    _fm_ = HelixScene._fm_.copy()
    _fm_.update(
            Node = MatuiNode,
            SGPass = MatuiSceneGraphPass,
            )

    _sgPassTypes_ = [
        ('load', True),
        ('pre-render', False),
        ('render', False),

        ('resize', False),

        ('pre-select', False),
        ('select', False),

        ('animate', False),
        ]

    _sgPassTriggers_ = [
        ('render', ['load', 'pre-render'], []),
        ('resize', ['load'], []),
        ('select', ['load', 'pre-select'], []),
        ('animate', [], ['render']),
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
            return self.sg_pass('animate', info)

