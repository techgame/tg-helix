#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2006  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from numpy.random import random
from TG.observing import ObservableObject, ObservableTypeParticipant

from TG.helixui.bridges.wx.basic import BasicRenderSkinModel
from TG.helixui.stage.scene import HelixUIScene, HelixSceneCommand
from TG.helixui.actors.basic import HelixActor, Widget
from TG.helixui.actors.visitor import IHelixVisitor

from TG.openGL.raw import gl, glu, glext
from TG.openGL.raw.gl import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RenderViewFactoryVisitor(IHelixVisitor):
    def visitScene(self, scene):
        return self.visitActor(scene)
    def visitActor(self, actor):
        viewFactoryMap = self.viewFactoryMap
        for key in actor.allVisitKeys:
            viewFactory = viewFactoryMap.get(key, None)
            if viewFactory is not None:
                return viewFactory(actor)
        else:
            return None

    viewFactoryMap = None
    def addViewForKeys(self, renderViewKlass, allViewKeys):
        viewFactoryMap = self.viewFactoryMap
        if viewFactoryMap is None:
            viewFactoryMap = {}
            self.viewFactoryMap = viewFactoryMap

        for key in allViewKeys:
            if key in viewFactoryMap:
                raise KeyError("Key %r already exists in viewFactoryMap")
            viewFactoryMap[key] = renderViewKlass

class RenderSceneCommand(HelixSceneCommand):
    action = 'render'

    def __init__(self, scene):
        self.scene = scene

    def perform(self, scene, **kw):
        getViewForActor = self.getViewForActor

        for actor in scene.items:
            view = getViewForActor(actor)
            if view is not None:
                view.render(actor)

        return True

    def getViewForActor(self, actor):
        try: return actor.__view
        except AttributeError: pass

        view = self.createViewForActor(actor)
        actor.__view = view
        return view
    
    def createViewForActor(self, actor):
        return actor.accept(self.viewFactoryVisitor)

    viewFactoryVisitor = RenderViewFactoryVisitor()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Actors
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ClearBuffers(HelixActor):
    color = (0.01, 0.01, 0.01, 0.0)
    depth = 1.0

class TestWidget(Widget):
    color = (1.0, 0.0, 0.0, 0.8)
    v = [[-0.5, -0.5, 0.], [0.5, -0.5, 0.], [0.5, 0.5, 0.], [-0.5, 0.5, 0.]]

    def __init__(self):
        self.color = random(4)
        self.v = random(3*3).reshape((3,3)) * 2. - 1.

    def recolor(self):
        self.color = (self.color + (random(4)/100)) % 1.0
    def reshape(self):
        self.v = random(3*3).reshape((3,3)) * 2. - 1.

    def randomly(self):
        if random() > 0.01:
            self.recolor()
        else:
            self.reshape()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Views
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BuildVisitTypeViews(ObservableTypeParticipant):
    def __init__(self, host=None):
        self.host = host
    def onObservableClassInit(self, selfAttrName, renderViewKlass):
        self.host.addViewForKeys(renderViewKlass, renderViewKlass.viewForKeys)

class HelixView(ObservableObject):
    pass

class RenderView(HelixView):
    _buildViews_ = BuildVisitTypeViews(RenderSceneCommand.viewFactoryVisitor)
    viewForKeys = []

    singleton = None
    def __new__(klass, actor):
        result = klass.singleton
        if result is None:
            result = HelixView.__new__(klass, actor)
            klass.singleton = result
        return result

    def __init__(self, actor):
        pass

    def render(self, actor):
        raise NotImplementedError('Subclass Responsibility: %r' % (self,))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ViewportBoundsView(RenderView):
    viewForKeys = ['ViewportBounds'] 

    def render(self, actor):
        glViewport(*actor.xywh())

class ClearBuffersView(RenderView):
    viewForKeys = ['ClearBuffers']

    def render(self, actor):
        glEnable(GL_DEPTH_TEST)

        glEnable(GL_COLOR_MATERIAL)
        glShadeModel(GL_SMOOTH)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glClearColor(*actor.color)
        glClearDepth(actor.depth)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

class TestWidgetView(RenderView):
    viewForKeys = ['TestWidget']

    def render(self, actor):
        glColor4f(*actor.color)
        glBegin(GL_TRIANGLES)
        for e in actor.v:
            glVertex3f(*e)
        glEnd()
        actor.randomly()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestScene(HelixUIScene):
    def loadCommands(self):
        super(TestScene, self).loadCommands()
        self.addCommand(RenderSceneCommand(self))

    def loadScene(self):
        super(TestScene, self).loadScene()
        self.items.extend([
                ClearBuffers(),
                ])
        self.items.extend(TestWidget() for e in xrange(2000))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestRenderSkinModel(BasicRenderSkinModel):
    SceneFactory = TestScene

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    model = TestRenderSkinModel()
    model.skinModel()

