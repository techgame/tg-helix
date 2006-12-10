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
    scene = ObservableProperty(None)
    @scene.fget
    def getScene(self, _paGet_):
        scene = _paGet_()
        if scene is None:
            scene = self.findScene()
            self.scene = scene
        return scene

    @scene.fset
    def setScene(self, scene, _paSet_):
        lastScene = _paSet_.fget()
        if lastScene is not None:
            self.sceneShutdown()
        _paSet_(scene)
        if scene is not None:
            self.sceneSetup()

    def findScene(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

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

