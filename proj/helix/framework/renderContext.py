#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
        self.setCurrent()
        self.scene.setup(self)
    def sceneShutdown(self):
        self.setCurrent()
        self.scene.shutdown(self)
    def sceneResize(self, viewportSize):
        self.setCurrent()
        self.scene.resize(self, viewportSize)
    def sceneRefresh(self):
        self.setCurrent()
        if self.scene.refresh(self):
            self.swapBuffers()

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

