#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import with_statement
from contextlib import contextmanager

from TG.observing import Observable, ObservableProperty

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderContext(Observable):
    scene = ObservableProperty()
    @scene.fset
    def setScene(self, scene, _propSet_):
        lastScene = self.scene
        if lastScene is not None:
            self.sceneShutdown()
        _propSet_(scene)
        if scene is not None:
            self.sceneSetup()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def sceneSetup(self):
        with self.sceneInContext() as scene:
            viewportSize = self.getMaxViewportSize()
            scene.setup(viewportSize)
    def sceneShutdown(self):
        with self.sceneInContext() as scene:
            scene.shutdown()
    def sceneResize(self, viewportSize):
        with self.sceneInContext() as scene:
            scene.resize(viewportSize)
    def sceneRefresh(self):
        with self.sceneInContext() as scene:
            if scene.refresh():
                self.swapBuffers()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    @contextmanager
    def sceneInContext(self):
        self.setCurrent()
        scene = self.scene
        scene.enterContext(self)
        yield scene
        scene.exitContext(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getMaxViewportSize(self):
        """getMaxViewportSize is provided by concrete implementations"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def setCurrent(self):
        """setCurrent is provided by concrete implementations"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def swapBuffers(self):
        """swapBuffers is provided by concrete implementations"""
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

