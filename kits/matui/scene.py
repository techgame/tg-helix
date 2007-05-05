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
    def _getNodeFromScene(self, scene):
        node = scene.root.newParent()
        node.info = 'sgp:' + self.passKey
        node.pre = node.insertNew(0)
        node.pre.info = 'sgp:pre-'+self.passKey
        node.post = node.addNew()
        node.post.info = 'sgp:post-'+self.passKey
        return node

    def sgBindOp(self, hostNode, opKey):
        hostNode.bindPass.add(opKey, self._sgBindPass_)

    def _sgBindPass_(self, node, ct, srm):
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

    _sgPassTree_ = [
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

    def sgPassConfig(self, sg_passes):
        for passKey, preKeys, postKeys in self._sgPassTree_:
            sgp = sg_passes[passKey]

            if preKeys:
                hostNode = sgp.node.pre
                for dk in preKeys:
                    dp = sg_passes[dk] 
                    dp.sgBindOp(hostNode, passKey)

            if postKeys:
                hostNode = sgp.node.pre
                for dk in postKeys:
                    dp = sg_passes[dk] 
                    dp.sgBindOp(hostNode, passKey)

    def sg_resize(self, info={}):
        return self.sg_pass('resize', info)
    def sg_render(self, info={}):
        return self.sg_pass('render', info)
    def sg_select(self, info={}):
        return self.sg_pass('select', info)

    animate = False
    def sg_animate(self, info={}):
        if self.animate: 
            return self.sg_pass('animate', info)

