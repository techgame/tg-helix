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

from __future__ import with_statement

from TG.kvObserving import KVProperty
from TG.geomath.data.kvBox import KVBox

from TG.freetype2.face import FreetypeFaceIndex
from TG.openGL.raw import gl
from TG.openGL.text import FontRect, Font2d, textLayout

from ..stage import ExpressGraphOp
from .base import Layer, LayerResources, LayerRenderOp
from .. import mesh

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TextLayerRenderOp(LayerRenderOp):
    def render(self, sgo):
        res = self.res
        res.updateText()

        gl.glPushMatrix()
        s = res.fscale.p1[1]
        gl.glScalef(s, s, s)

        res.texture()
        res.color()
        res.text()
        res.notexture()

        gl.glPopMatrix()

class TextLayerResizeOp(ExpressGraphOp):
    def __init__(self, actor, sgNode):
        self.box = actor.box
        self.fscale = actor.fscale

    def bindPass(self, node, sgo):
        return [self.resize], None
    def resize(self, sgo):
        self.fscale.p0 = sgo.viewportSize
        self.fscale.p1 = self.box.size/sgo.viewportSize

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TextLayerResources(LayerResources):
    FontFactory = FontRect
    ftFaceIndex = FreetypeFaceIndex.forSystem()

    def __init__(self, actor):
        self.actor = actor

        self.fscale = actor.fscale

        self.mcolor = actor.color
        self.mtext = mesh.BufferedTextMesh()
        self.text = self.mtext.render

        actor.kvpub.add('@font', self.updateFont)
        actor.kvpub.add('@text', self.markTextMeshDirty)

    meshDirty = True
    def markTextMeshDirty(self, *args, **kw):
        self.meshDirty = True
    
    def updateFont(self, actor, kvkey=None):
        self.meshDirty = True

        faceName, _, faceStyle = actor.fontFace.partition('#')
        face = self.ftFaceIndex.face(faceName, faceStyle or 0)
        self.font = self.FontFactory.fromFace(face, actor.fontSize)

        self.mtexture = self.font.texture
        self.mtexture.deselect()
        self.texture = self.mtexture.select
        self.notexture = self.mtexture.deselect

    def updateText(self):
        if not self.meshDirty:
            return

        actor = self.actor
        textLayout = actor.textLayout
        textLayout.textData = self.font.textData(actor.text)

        geom = textLayout.layoutMeshInBox(actor.box)
        self.mtext.update(geom)
        self.meshDirty = False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TextLayer(Layer):
    """
    Text Layer -- Uniform for now?
        Size
        Regular, Bold, Italic, Bold Italic
        Alignment
            Animation
        Underline, Strike?

        Outline
        Shadow
            Color
            With shader for softness?
        Leading -- space between lines
        Tracking -- kerning scale
    """

    kvpub = Layer.kvpub.copy()

    sceneGraphOps = dict(render=TextLayerRenderOp, resize=TextLayerResizeOp)
    resData = TextLayerResources.property()

    fscale = KVBox([0,0])

    text = KVProperty('')
    fontFace = KVProperty('Courier')
    fontSize = KVProperty(64)
    kvpub.depend('@text', ['box', 'textLayout', 'text'])
    kvpub.depend('@font', ['fontSize', 'fontFace'])

    def __init__(self, text=None, color=None, fontFace=None, fontSize=None):
        Layer.__init__(self, color)
        with self.kvpub:
            self.textLayout = textLayout.TextLayout()

            if text is not None:
                self.text = text

            if fontFace is not None:
                self.fontFace = fontFace
            if fontSize is not None:
                self.fontSize = fontSize

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getWrapMode(self):
        return self.textLayout.wrapMode
    def setWrapMode(self, wrapMode):
        self.textLayout.wrapMode = wrapMode
        self.kvpub('textLayout')
    wrapMode = property(getWrapMode, setWrapMode)

    def getAlign(self):
        return self.textLayout.align
    def setAlign(self, align):
        self.textLayout.align = align
        self.kvpub('textLayout')
    align = property(getAlign, setAlign)

