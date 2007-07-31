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
from TG.helix.actors.scene import HelixScene, SceneRenderManager
from .node import MatuiNode

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Scene
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiSceneRenderManager(SceneRenderManager):
    pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MatuiScene(HelixScene, KVObject):
    _fm_ = HelixScene._fm_.copy()
    _fm_.update(
            Node = MatuiNode,
            SceneRenderManager = MatuiSceneRenderManager
            )

    _sgPassTypes_ = [
        ('load', True),

        ('pre-render', False),
        ('render', False),

        ('resize', False),

        ('pre-pick', False),
        ('pick', False),

        ('animate', False),
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

    def sg_resize(self, info=None):
        self.srm.invalidate()
        return self.sg_pass('resize', info)
    def sg_render(self, info=None):
        return self.sg_pass('render', info)
    def sg_pick(self, info=None):
        return self.sg_pass('pick', info)
    def sg_load(self):
        return self.sg_pass('load')

    animate = False
    def sg_animate(self, info=None):
        if self.animate: 
            self.sg_pass('animate', info)

        if self.srm.invalidated:
            return self.sg_render(info)

