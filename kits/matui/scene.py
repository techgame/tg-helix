#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.metaObserving import OBFactoryMap
from TG.kvObserving import KVObject

from TG.helix.actors import sceneManagers
from TG.helix.actors.scene import HelixScene, SceneAnimationEventHandler

from .node import MatuiNode

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiScene(HelixScene, KVObject):
    _fm_ = OBFactoryMap(Node=MatuiNode)
    _sgPassFactories_ = {
        'load': sceneManagers.LoadManager,
        'render': sceneManagers.RenderManager,
        'resize': sceneManagers.ResizeManager,
        'select': sceneManagers.SelectManager,
        }

    def setupEvtSources(self, evtSources=[]):
        evtRoot = HelixScene.setupEvtSources(self, evtSources)
        evtRoot.visit(SceneAnimationEventHandler(self))
        return evtRoot

    def setupSceneGraph(self):
        rootNode = self._fm_.Node(scene=self)
        for sgPassKey, sgPassFactory in self._sgPassFactories_.items():
            mgrNode = rootNode.new()
            mgrNode.add(rootNode)

            self.sgManagers[sgPassKey] = sgPassFactory(self, mgrNode)

        self.rootNode = rootNode

    def _sgRender_(self, viewport):
        self.sgManagers['load'](viewport)
        return self.sgManagers['render'](viewport)

