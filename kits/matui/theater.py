##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2007  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from TG.kvObserving import KVObject
from TG.helix.actors.theater import HelixTheater, SceneRenderManager
from TG.helix.actors.sceneGraphPass import SceneGraphPass, SingleSceneGraphPass, EventSceneGraphPass
from .node import MatuiNode

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiSceneRenderManager(SceneRenderManager, KVObject):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiTheater(HelixTheater, KVObject):
    _fm_ = HelixTheater._fm_.copy()
    _fm_.update(
            Node = MatuiNode,
            SceneRenderManager = MatuiSceneRenderManager
            )

    _sgPassTypes_ = [
        ('load', SingleSceneGraphPass),

        ('pre-render', SceneGraphPass),
        ('render', SceneGraphPass),

        ('resize', SceneGraphPass),

        ('pre-pick', SceneGraphPass),
        ('pick', SceneGraphPass),

        ('animate', SceneGraphPass),

        ('key', EventSceneGraphPass),
        ('mouse', EventSceneGraphPass),
        ]

    _sgPassTriggers_ = [
        ('render', ['load', 'pre-render'], []),
        ('resize', ['load'], []),
        ('pick', ['load', 'pre-pick'], []),
        ('animate', ['load'], []),
        ]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setupEvtSources(self):
        evtRoot = self.evtRoot
        evtRoot.add('viewport-size', self.sg_resize)
        evtRoot.add('viewport-paint', self.sg_render)
        evtRoot.add('timer', self.sg_animate)

        evtRoot.add('mouse', self.sg_mouse)
        evtRoot.add('key', self.sg_key)

    def sg_load(self):
        return self.sg_pass('load')
    def sg_resize(self, info=None):
        self.srm.invalidate()
        return self.sg_pass('resize', info)
    def sg_render(self, info=None):
        return self.sg_pass('render', info)
    def sg_pick(self, info=None):
        return self.sg_pass('pick', info)
    def sg_mouse(self, info=None):
        return self.sg_pass('mouse', info)
    def sg_key(self, info=None):
        return self.sg_pass('key', info)

    animate = False
    def sg_animate(self, info=None):
        if self.animate: 
            self.sg_pass('animate', info)

        if self.srm.invalidated:
            return self.sg_render(info)

