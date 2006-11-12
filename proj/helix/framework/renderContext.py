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
        scene = self.scene
        if scene is not None:
            scene.setup(self)
    def sceneShutdown(self):
        self.setCurrent()
        scene = self.scene
        if scene is not None:
            scene.shutdown(self)
    def sceneResize(self, viewportSize):
        self.setCurrent()
        scene = self.scene
        if scene is not None:
            scene.resize(self, viewportSize)
        else: print 'scene is:', repr(scene)
    def sceneRefresh(self):
        self.setCurrent()
        scene = self.scene
        if scene is not None:
            if scene.refresh(self):
                self.swapBuffers()
        else: print 'scene is:', repr(scene)

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
