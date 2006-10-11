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
from TG.helixui.actors.basic import ViewportBounds

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SceneCommand(Observable):
    action = None

    def perform(self, scene, **kw):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

class SceneVisitor(SceneCommand):
    action = None

    def __init__(self, visitor, action=None):
        self.visitor = visitor
        if action is None:
            self.action = getattr(visitor, 'action', None)

    # visitor is an instance of an actors.visitor.HelixVisitor
    visitor = None 
    def perform(self, scene, **kw):
        return scene.accept(self.visitor)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixScene(HelixActor):
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

class HelixUIScene(HelixScene):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Scene Commands 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    managers = ObservableDict.property()
    def getManagerFor(self, resourceKind):
        return self.managers[resourceKind]
    def addManager(self, manager, resourceKind=None):
        if resourceKind is None:
            resourceKind = command.resourceKind
        self.managers[resourceKind] = manager

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    commands = ObservableDict.property()

    def getCommandFor(self, action):
        return self.commands[action]
    def addCommand(self, command, action=None):
        if action is None:
            action = command.action
        self.commands[action] = command
    def performCommand(self, action, scene, **kw):
        cmd = self.getCommandFor(action)
        return cmd.perform(scene, **kw)

    def render(self, **kw):
        return self.performCommand('render', self, **kw)
    def selectPick(self, **kw):
        return self.performCommand('selectPick', self, **kw)
    def selectColor(self, **kw):
        return self.performCommand('selectColor', self, **kw)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    viewport = None
    ViewportFactory = ViewportBounds

    def init(self):
        self.loadManagers()
        self.loadCommands()

    def loadManagers(self):
        pass

    def loadCommands(self):
        pass

    def setup(self, renderContext):
        self.ctx = renderContext
        self.loadScene()

    def loadScene(self):
        self.items = self.ItemsFactory()
        self.viewport = self.items.add(self.ViewportFactory())

    def shutdown(self, renderContext):
        self.ctx = renderContext
        self.unloadScene(self)
        self.ctx = None

    def unloadScene(self):
        self.items.clear()
        del self.viewport

    def resize(self, renderContext, size):
        self.ctx = renderContext
        self.viewport.setViewportSize(size)
    def refresh(self, renderContext):
        self.ctx = renderContext
        result = self.refreshRender()
        return result

    def refreshRender(self):
        return self.render()

