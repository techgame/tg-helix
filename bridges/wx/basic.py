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

import TG.openGL.raw
from TG.skinning.toolkits.wx import wx, wxSkinModel, XMLSkin

from . import viewLoader

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
            <panel>
                <layout>
                    <opengl-canvas size='100,100'>
                        ctx.model.setupCanvas(elem, obj)
                    </opengl-canvas>
                </layout>
            </panel>
        </layout>
        ctx.model.setupFrame(obj)
    </frame>
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class BasicRenderSkinModel(wxSkinModel):
    xmlSkin = xmlSkin

    frameTitle = 'Basic wxPython HelixUI Render Skin'
    clientSize = (800, 800)
    minSize = (200, 200)
    fullscreen = False

    def setupStage(self, options, scene):
        self.options = options
        self.scene = scene

    SceneHostViewLoader = viewLoader.SceneHostViewLoader
    def setupCanvas(self, canvasElem, canvasObj):
        canvasObj.SetCurrent()
        # Reload the opengl raw api to support windows
        TG.openGL.raw.apiReload()

        self.SceneHostViewLoader.load(canvasObj, self.options, self.scene)

    def setupFrame(self, frame):
        self.frame = frame
        if self.frameTitle:
            frame.SetTitle(self.frameTitle)
        if self.clientSize:
            frame.SetClientSize(self.clientSize)
        if self.minSize:
            frame.SetMinSize(self.minSize)

        if self.fullscreen:
            frame.ShowFullScreen(True)

    def close(self):
        self.frame.Close()

    def showAndRun(self):
        self.skinModel()

