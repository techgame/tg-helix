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

from TG.skinning.toolkits.wx import wx, wxSkinModel, XMLSkin
from TG.kvObserving import KVObject, KVProperty
from TG.helix.bridges.wx import viewLoader

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Constants / Variables / Etc. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

xmlSkin = XMLSkin("""<?xml version='1.0'?>
<skin xmlns='TG.skinning.toolkits.wx'>
    <style>
        frame {
            title: 'Theater';
            frame-main:1;
            locking:0;
            show: True;
            }
        frame>layout {
            layout-cfg:1,EXPAND;
            }
        frame>layout>panel {
            layout-cfg:1,EXPAND;
            }

        opengl-canvas {
            layout-cfg:1,EXPAND; 
            gl-style:WX_GL_RGBA, WX_GL_DOUBLEBUFFER, WX_GL_DEPTH_SIZE, 8;
            size: 1024,768;
            }
    </style>

    <frame>
        <menubar>
            <menu text='View'>
                <item text='Full Screen\tCtrl-F' help='Shows My Frame on the entire screen'>
                    <event>
                        if ctx.frame.IsFullScreen():
                            ctx.frame.ShowFullScreen(False)
                        else: ctx.frame.ShowFullScreen(True)
                    </event>
                    <event type='EVT_UPDATE_UI'>
                        if ctx.frame.IsFullScreen():
                            obj.SetText('Restore from Full Screen\tCtrl-F')
                        else: obj.SetText('Full Screen\tCtrl-F')
                    </event>
                </item>
            </menu>
        </menubar>

        <layout>
            <panel>
                <layout>
                    <opengl-canvas>
                        ctx.model.setupCanvas(elem, obj)
                    </opengl-canvas>
                </layout>
            </panel>
        </layout>
        obj.Center()
    </frame>
</skin>
""")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TheaterHost(wxSkinModel, KVObject):
    xmlSkin = xmlSkin
    fullscreen = False
    runSkin = False

    stage = KVProperty(None)

    def __init__(self, stage=None, bSkinModel=True):
        KVObject.__init__(self)
        wxSkinModel.__init__(self)

        self.stage = stage

        if bSkinModel:
            if wx.GetApp() is None:
                raise RuntimeError("TheaterHost cannot be created before StudioHost")
            self.skinModel()

    SceneHostViewLoader = viewLoader.SceneHostViewLoader
    def setupCanvas(self, canvasElem, canvasObj):
        self.SceneHostViewLoader.load(canvasObj, self.stage, self.stage.scene)

