#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.observing import Observable, ObservableDict

from TG.helixui.actors.helix import HelixActor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixSceneCommand(Observable):
    action = None

    def performCommand(self, action, scene, **kw):
        return self.perform(scene, **kw)
    def perform(self, scene, **kw):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixSceneBase(HelixActor):
    """A Helix scene is the root rendering object, which is simply a composite
    of all the actors below it.  It acts as a mediator, keeping links to event
    roots relevant to the scene.  
    
    It can also processes the different rendering modes to support picking, or
    picking through rendering colours.
    """

    visitKind = "Scene"

    #~ IHelixScene ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setup(self, renderContext): pass
    def shutdown(self, renderContext): pass
    def resize(self, renderContext, size): pass
    def refresh(self, renderContext): pass

    def accept(self, visitor):
        return visitor.visitScene(self)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixScene(HelixSceneBase):
    def init(self):
        self.items = self.ItemsFactory()
        self.loadManagers()
        self.loadCommands()

    def loadManagers(self): pass
    def loadCommands(self): pass
    def loadScene(self): pass

    def setup(self, renderContext):
        self.ctx = renderContext
        self.loadScene()
        self.performRenderInitial()

    def shutdown(self, renderContext):
        self.ctx = renderContext
        self.unloadScene(self)
        self.ctx = None

    def unloadScene(self):
        self.items.clear()
        del self.viewport

    def resize(self, renderContext, size):
        self.ctx = renderContext
        return self.performResize(size=size)
    def refresh(self, renderContext):
        self.ctx = renderContext
        return self.performRenderRefresh()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    commands = ObservableDict.property()

    def getCommandFor(self, action):
        return self.commands[action]
    def addCommand(self, action, command):
        self.commands[action] = command
    def performCommand(self, action, scene, **kw):
        cmd = self.getCommandFor(action)
        return cmd(action, scene, **kw)

    def performResize(self, **kw):
        return self.performCommand('resize', self, **kw)
    def performRenderInitial(self, **kw):
        return self.performCommand('renderInitial', self, **kw)
    def performRenderRefresh(self, **kw):
        return self.performCommand('renderRefresh', self, **kw)
    def performSelectByPick(self, **kw):
        return self.performCommand('selectPick', self, **kw)
    def performSelectByColor(self, **kw):
        return self.performCommand('selectColor', self, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    managers = ObservableDict.property()
    def getManagerFor(self, resourceKind):
        return self.managers[resourceKind]
    def addManager(self, manager, resourceKind=None):
        if resourceKind is None:
            resourceKind = command.resourceKind
        self.managers[resourceKind] = manager

