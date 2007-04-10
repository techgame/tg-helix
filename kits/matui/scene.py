#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.kvObserving import KVObject, KVProperty, KVList

from TG.helix.actors import HelixNode
from TG.helix.actors import sceneManagers
from TG.helix.actors.scene import HelixScene, SceneAnimationEventHandler

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Node
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiNode(HelixNode):
    _sgOpRequired_ = {'render': None, 'resize': None, 'select':'render'}
    def __init__(self):
        self.parents = KVList()
        self.children = KVList()

    @classmethod
    def itemAsNode(klass, item, create=True):
        if item.isNode():
            return item

        node = item._sgNode_
        if node is None and create:
            node = item._sgNewNode_(klass.new, klass._sgOpRequired_)
        return node

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiScene(HelixScene, KVObject):
    _sgPassManagers_ = {
        'render': sceneManagers.RenderManager,
        'resize': sceneManagers.ResizeManager,
        'select': sceneManagers.SelectManager,
        }

    def setupEvtSources(self, evtSources=[]):
        evtRoot = HelixScene.setupEvtSources(self, evtSources)
        evtRoot.visit(SceneAnimationEventHandler(self))
        return evtRoot

    def setupSceneGraph(self):
        rootNode = MatuiNode.createRootForScene(self)
        for sgPassKey, sgPassFactory in self._sgPassFactories_.items():
            self.sgManagers[sgPassKey] = sgPassFactory(self, rootNode)

