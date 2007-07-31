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

import TG.openGL.raw
from TG.skinning.toolkits.wx import wx, wxSkinModel, XMLSkin

from . import viewLoader

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xmlSkin = XMLSkin("""<?xml version='1.0'?>
<skin xmlns='TG.skinning.toolkits.wx'>
    <style>
        frame {title: "Helix Host"; frame-main:1; locking:0; show: False}
        frame>layout {layout-cfg:1,EXPAND}
        frame>layout>panel {layout-cfg:1,EXPAND}

        opengl-canvas {
            layout-cfg:1,EXPAND; 
            gl-style:WX_GL_RGBA, WX_GL_DOUBLEBUFFER, WX_GL_DEPTH_SIZE, 8;
            }
    </style>

    <frame ctxobj='model.frame'>
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
                        else: obj.SetText('Full Screen\tCtrl-F')
                    </event>
                </item>
            </menu>
        </menubar>

        ctx.model.adjPosition()
        if wx.Platform == '__WXMSW__':
            obj.Show(True)

        <layout>
            <panel>
                <layout>
                    <opengl-canvas gl-context='ctx.model.getGLContext()'>
                        ctx.model.setupCanvas(elem, obj)
                    </opengl-canvas>
                </layout>
            </panel>
        </layout>
    </frame>
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class HelixHost(wxSkinModel):
    xmlSkin = xmlSkin
    runSkin = False

    def __init__(self, scene, options=None):
        self.scene = scene

        r = {}
        if options is not None:
            r.update(options)
        self.options = r

        wxSkinModel.__init__(self)
        self.skinModel()

    TheaterHostViewLoader = viewLoader.TheaterHostViewLoader
    def setupCanvas(self, canvasElem, canvasObj):
        self.setGLContext(canvasObj.GetContext())
        canvasObj.SetCurrent()
        # Reload the opengl raw api to support windows
        TG.openGL.raw.apiReload()

        if self.scene is not None:
            self.TheaterHostViewLoader.load(canvasObj, self.options, self.scene)

    _glcontext = None
    @classmethod
    def getGLContext(klass):
        glcontext = klass._glcontext
        if glcontext:
            return glcontext
    @classmethod
    def setGLContext(klass, glcontext):
        klass._glcontext = glcontext

    def show(self, visible=True):
        self.frame.Show(visible)

    def adjPosition(self):
        self.frame.SetClientSize(self.options.get('size', (1024, 768)))
        self.frame.Center()

