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
        if self.scene is not None:
            self.scene.setup(self)
    def sceneShutdown(self):
        self.setCurrent()
        if self.scene is not None:
            self.scene.shutdown(self)
    def sceneRefresh(self):
        self.setCurrent()
        if self.scene is not None:
            if self.scene.refresh(self):
                self.swapBuffers()
    def sceneResize(self, viewportSize):
        self.setCurrent()
        if self.scene is not None:
            self.scene.resize(self, viewportSize)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getMaxViewportSize(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def setCurrent(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))
    def swapBuffers(self):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))


