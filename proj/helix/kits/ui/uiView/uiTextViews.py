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

from TG.openGL.data.bufferObjects import ArrayBuffer
from TG.openGL.text import textWrapping, textLayout

from TG.openGL.raw import gl

from .uiViewBase import UIView

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIFontView(UIView):
    viewForKeys = ['UIFont']

    partsByName = ['font']

    def init(self, uiFont):
        UIView.init(self, uiFont)
        self.update(uiFont, self.partsByName)

    def _onViewableChange(self, viewable, attr):
        UIView._onViewableChange(self, viewable, attr)
        if attr in partsByName:
            self.update(viewable, attr)

    def update(self, uiFont, partsByName):
        for pname in partsByName:
            if pname == 'font':
                self.texFont = uiFont.font.texture
                self.textData = uiFont.font.textData

    def select(self):
        self.texFont.select()
    def deselect(self):
        self.texFont.deselect()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UITextView(UIView):
    viewForKeys = ['UIText']

    partsByName = ['color', 'font', 'wrapMode', 'text', 'box']

    TextDisplayFactory = None #TextBufferedDisplay
    WrapModeMap = textWrapping.wrapModeMap.copy()
    wrapper = WrapModeMap['basic']
    layoutText = textLayout.TextLayout().layout

    def init(self, uiText):
        UIView.init(self, uiText)
        self.uiText = uiText
        self.text = self.TextDisplayFactory()
        self.update(uiText, self.partsByName)

    def _onViewableChange(self, viewable, attr):
        UIView._onViewableChange(self, viewable, attr)
        self.update(viewable, [attr])

    def update(self, uiText, parts):
        for pname in parts:
            if pname == 'color':
                self.color = self.viewFactory(uiText.color)
            elif pname == 'font':
                self.font = self.viewFactory(uiText.font)
            elif pname == 'wrapMode':
                self.wrapper = self.WrapModeMap[uiText.wrapMode]
            elif pname == 'box':
                uiText.box._pub_.add(self.updateBox)
        self.enqueue(self.updateText, uiText)

    def updateBox(self, box, boxName):
        self.enqueue(self.updateText, self.uiText)
    def updateText(self, uiText):
        textData = self.font.textData(uiText.text)
        geom = self.layoutText(uiText, textData, self.wrapper)
        self.text.update(geom)

    def render(self):
        UIView.render(self)
        self.color.render()

        self.font.select()
        self.text.render()
        self.font.deselect()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ TextDisplay
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TextDisplay(object):
    geometry = None
    def update(self, geometry):
        self.geometry = geometry

    def render(self):
        geom = self.geometry
        gl.glInterleavedArrays(geom.glTypeId, 0, geom.ctypes)
        gl.glDrawArrays(geom.drawMode, 0, geom.size)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TextBufferedDisplay(object):
    geometry = None
    buffer = None
    def update(self, geometry):
        self.geometry = geometry

        # push the data to the card
        buff = self.buffer 
        if buff is None:
            buff = ArrayBuffer('dynamicDraw')
            self.buffer = buff

        buff.bind()
        buff.sendData(geometry)
        buff.unbind()

    def render(self, glColor4f=gl.glColor4f):
        geom = self.geometry
        if not geom: return

        buff = self.buffer
        buff.bind()

        gl.glInterleavedArrays(geom.glTypeId, 0, 0)
        gl.glDrawArrays(geom.drawMode, 0, geom.size)

        ## Font rect/outline highlighting code:
        #if 0:
        #    gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)

        #    gl.glColor4f(1, .9, .9, .2)
        #    gl.glDrawArrays(geom.drawMode, 0, geom.size)

        #    gl.glColor4f(1, .4, .4, .4)
        #    gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        #    gl.glDrawArrays(geom.drawMode, 0, geom.size)
        #    gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

        #    gl.glColor4f(1, 1, 1, 1)

        buff.unbind()

UITextView.TextDisplayFactory = TextBufferedDisplay

