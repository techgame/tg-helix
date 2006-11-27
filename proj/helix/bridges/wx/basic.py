#!/usr/local/bin/python2.5
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import sys
import time

from TG.skinning.toolkits.wx import wxSkinModel, XMLSkin

from renderContext import wxRenderContext

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xmlSkin = XMLSkin("""<?xml version='1.0'?>
<skin xmlns='TG.skinning.toolkits.wx'>
    <style>
        frame {frame-main:1; locking:0; show: True}
        frame>layout {layout-cfg:1,EXPAND}
        frame>layout>panel {layout-cfg:1,EXPAND}

        opengl-canvas {
            layout-cfg:1,EXPAND; 
            gl-style:WX_GL_RGBA, WX_GL_DOUBLEBUFFER, WX_GL_DEPTH_SIZE, 8;
            }
    </style>

    <frame>
        <menubar>
            <menu text='View'>
                <item text='Full Screen\tCtrl-F' help='Shows My Frame on the entire screen'>
                    <event>
                        if ctx.frame.IsFullScreen():
                            ctx.frame.ShowFullScreen(False)
                        else:
                            ctx.frame.ShowFullScreen(True)
                    </event>
                    <event type='EVT_UPDATE_UI'>
                        if ctx.frame.IsFullScreen():
                            obj.SetText('Restore from Full Screen\tCtrl-F')
                        else:
                            obj.SetText('Full Screen\tCtrl-F')
                    </event>
                </item>
            </menu>
        </menubar>

        <layout>
            <opengl-canvas>
                ctx.model.setupCanavs(elem, obj)
            </opengl-canvas>
        </layout>
        obj.SetClientSize(ctx.model.clientSize)
        if ctx.model.minSize:
            obj.SetMinSize(ctx.model.minSize)
    </frame>
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BasicRenderSkinModel(wxSkinModel):
    xmlSkin = xmlSkin
    clientSize = (800, 800)
    minSize = None
    frameTitle = 'Basic wxPython HelixUI Render Skin'

    renderContext = None
    RenderContextFactory = wxRenderContext
    def setupCanavs(self, canvasElem, canvasObj):
        ctx = self.RenderContextFactory(canvasObj)
        ctx.scene = self.scene
        self.renderContext = ctx

    _scene = None
    def getScene(self):
        if self.renderContext is not None:
            return self.renderContext.scene
        else: return self._scene
    def setScene(self, scene):
        if self.renderContext is not None:
            self.renderContext.scene = scene
        else: self._scene = scene
    scene = property(getScene, setScene)

    SceneFactory = None
    def createScene(self):
        return self.SceneFactory()

