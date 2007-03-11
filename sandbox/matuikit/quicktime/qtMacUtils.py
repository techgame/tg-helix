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

from struct import pack, unpack
import ctypes, ctypes.util
from ctypes import cast, byref, c_void_p, c_float, POINTER

import numpy

import aglUtils

from TG.openGL.raw import gl

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Libraries
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

libCoreFoundationPath = ctypes.util.find_library("CoreFoundation")
libCoreFoundation = ctypes.cdll.LoadLibrary(libCoreFoundationPath)

libQuickTimePath = ctypes.util.find_library("QuickTime")
libQuickTime = ctypes.cdll.LoadLibrary(libQuickTimePath)

libCoreVideoPath = ctypes.util.find_library("CoreVideo")
libCoreVideo = ctypes.cdll.LoadLibrary(libCoreVideoPath)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ QuickTime Stuff
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CFStringRef = ctypes.c_void_p
kCFStringEncodingUTF8 = 0x8000100

def asCFString(astr):
    utf8_astr = astr.encode('utf8')
    p_astr = ctypes.c_char_p(utf8_astr)
    cfs_astr = libCoreFoundation.CFStringCreateWithCString(0, p_astr, kCFStringEncodingUTF8)
    assert len(astr) == libCoreFoundation.CFStringGetLength(cfs_astr)
    return CFStringRef(cfs_astr)

CFURLRef = ctypes.c_void_p
def asCFURL(astr):
    cfs_astr = asCFString(astr)
    cfurl_astr = libCoreFoundation.CFURLCreateWithString(0, cfs_astr, None)
    return CFURLRef(cfurl_astr)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Boolean = ctypes.c_ubyte
booleanFalse = Boolean(0)
booleanTrue = Boolean(1)

c_appleid = ctypes.c_uint32
def fromAppleId(strAppleId): return unpack('!I', strAppleId)[0]
def toAppleId(intAppleId): return pack('!I', intAppleId)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class QTNewMoviePropertyElement(ctypes.Structure):
    _fields_ = [
        ('propClass', c_appleid),
        ('propID', c_appleid),
        ('propValueSize', (ctypes.c_uint32)),
        ('propValueAddress', ctypes.c_void_p),
        ('propStatus', (ctypes.c_int32)),
        ]
    
    @classmethod
    def new(klass, cid, pid, value):
        if hasattr(value, '_as_parameter_'):
            value = value._as_parameter_
        valueSize = ctypes.sizeof(type(value))
        p_value = cast(byref(value), c_void_p)
        return klass(
                fromAppleId(cid), 
                fromAppleId(pid), 
                valueSize,
                p_value, 0)

    @classmethod
    def fromProperties(klass, *properties):
        return klass.fromPropertyList(properties)

    @classmethod
    def fromPropertyList(klass, propList):
        propList = [klass.new(*p) for p in propList]
        return (klass*len(propList))(*propList)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def qtEnterMovies():
    libQuickTime.EnterMovies()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CVOpenGLTexture(object):
    texCoords = None
    texTarget = None
    texName = None

    def __init__(self, visualContext):
        self.texCoords = numpy.zeros((4,2), 'f')
        self._texCoordsAddresses = [tc.ctypes.data for tc in self.texCoords]
        assert len(self._texCoordsAddresses) == 4

        self.visualContext = visualContext
        self._cvTextureRef = c_void_p(0)

    def isNewImageAvailable(self):
        return libQuickTime.QTVisualContextIsNewImageAvailable(self.visualContext, None)
        

    def update(self, force=False):
        if not force and not self.isNewImageAvailable():
            return False

        libCoreVideo.CVOpenGLTextureRelease(self._cvTextureRef)
        cvTextureRef = c_void_p(0)
        self._cvTextureRef = cvTextureRef

        libQuickTime.QTVisualContextCopyImageForTime(self.visualContext, None, None, byref(cvTextureRef))

        self.texTarget = libCoreVideo.CVOpenGLTextureGetTarget(cvTextureRef)
        self.texName = libCoreVideo.CVOpenGLTextureGetName(cvTextureRef)

        # CVOpenGLTextureGetCleanTexCoords takes into account whether or not the texture is flipped
        libCoreVideo.CVOpenGLTextureGetCleanTexCoords(cvTextureRef, *self._texCoordsAddresses)
        #libCoreVideo.CVOpenGLTextureIsFlipped(cvTextureRef)

        self.movieSize = abs(self.texCoords[2]-self.texCoords[0])
        return True

    movieSize = None
    def renderDirect(self):
        if not self.texName:
            return False

        texCoords = self.texCoords
        w, h = texCoords[2]-texCoords[0]
        gl.glPushMatrix()
        if h<0:
            gl.glTranslatef(0, -h, 0)
            gl.glScalef(1, -1, 1)

        gl.glEnable(self.texTarget)
        gl.glBindTexture(self.texTarget, self.texName)
        gl.glBegin(gl.GL_QUADS)

        gl.glTexCoord2f(*texCoords[0])
        gl.glVertex2f(*texCoords[0])

        gl.glTexCoord2f(*texCoords[1])
        gl.glVertex2f(*texCoords[1])

        gl.glTexCoord2f(*texCoords[2])
        gl.glVertex2f(*texCoords[2])

        gl.glTexCoord2f(*texCoords[3])
        gl.glVertex2f(*texCoords[3])

        gl.glEnd()

        gl.glPopMatrix()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class QTOpenGLVisualContext(object):
    _as_parameter_ = None

    def __init__(self, bCreate=True):
        if bCreate:
            self.create()

    def create(self):
        if self._as_parameter_:
            return self

        cglCtx, cglPix = aglUtils.getCGLContextAndFormat()
        self._as_parameter_ = c_void_p()
        errqt = libQuickTime.QTOpenGLTextureContextCreate(None, cglCtx, cglPix, None, byref(self._as_parameter_))
        assert not errqt, errqt
        return self

    def process(self):
        libQuickTime.QTVisualContextTask(self)

    _texture = None
    def texture(self):
        tex = self._texture
        if tex is None:
            tex = CVOpenGLTexture(self)
            self._texture = tex
        return tex

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class QTMovie(object):
    def __init__(self, filePath=None):
        self.createContext()
        if filePath is not None:
            self.loadPath(filePath)

    def createContext(self):
        self.visualContext = QTOpenGLVisualContext()
        self.texMovie = self.visualContext.texture()
        
    def loadURL(self, fileURL):
        cfFileURL = asCFURL(fileURL)

        return self.loadFromProperties([
                ('dloc', 'cfur', cfFileURL),

                ('mprp', 'actv', booleanTrue),
                #('mprp', 'intn', booleanTrue),
                #('mins', 'aurn', booleanTrue),
                # No async for right now
                ('mins', 'asok', booleanTrue),

                ('ctxt', 'visu', self.visualContext),
                ])

    def loadPath(self, filePath):
        cfFilePath = asCFString(filePath)

        return self.loadFromProperties([
                ('dloc', 'cfnp', cfFilePath),

                ('mprp', 'actv', booleanTrue),
                #('mprp', 'intn', booleanTrue),
                #('mins', 'aurn', booleanTrue),
                # No async for right now
                ('mins', 'asok', booleanTrue),

                ('ctxt', 'visu', self.visualContext),
                ])

    def loadFromProperties(self, movieProperties):
        movieProperties = QTNewMoviePropertyElement.fromPropertyList(movieProperties)
        self._as_parameter_ = c_void_p()
        errqt = libQuickTime.NewMovieFromProperties(len(movieProperties), movieProperties, 0, None, byref(self._as_parameter_))

        if errqt:
            print
            print 'Movies Error:', libQuickTime.GetMoviesError()
            print 'Movie Properties::'
            for prop in movieProperties:
                print '   ', toAppleId(prop.propClass), toAppleId(prop.propID), prop.propStatus
            print
            print 
            raise Exception("Failed to initialize QuickTime movie from properties")
        elif 0:
            print 'Movie Properties::'
            for prop in movieProperties:
                print '   ', toAppleId(prop.propClass), toAppleId(prop.propID), prop.propStatus
            print
            self.printTracks()

        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def process(self, millisec=0):
        self.visualContext.process()
        return self.processMovieTask()

    def processMovieTask(self, millisec=0):
        return libQuickTime.MoviesTask(self, millisec)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getLoadState(self):
        return libQuickTime.GetMovieLoadState(self)

    def setLooping(self, looping=1):
        libQuickTime.GoToBeginningOfMovie(self)
        timeBase = libQuickTime.GetMovieTimeBase(self)
        libQuickTime.SetTimeBaseFlags(timeBase, looping) # loopTimeBase

        hintsLoop = 0x2
        libQuickTime.SetMoviePlayHints(self, hintsLoop, hintsLoop)

    def printTracks(self):
        trackMediaType = c_appleid()
        for trackIdx in xrange(libQuickTime.GetMovieTrackCount(self)):
            track = libQuickTime.GetMovieIndTrack(self, trackIdx)
            print 'track:', trackIdx, track
            if track:
                trackMedia = libQuickTime.GetTrackMedia(track)
                print '  media:', trackMedia
                if trackMedia:
                    libQuickTime.GetMediaHandlerDescription(trackMedia, byref(trackMediaType), 0, 0)
                    print '    ', toAppleId(trackMediaType)
                    #if trackMediaType[:] not in ('vide', 'soun'):
                    #    libQuickTime.SetTrackEnabled(track, False)
                    #    print 'disabled'
                    #else:
                    #    print 'enabled'
        print


    def start(self):
        libQuickTime.StartMovie(self)

    def stop(self):
        libQuickTime.StopMovie(self)

    def isActive(self):
        return libQuickTime.GetMovieActive(self)
    def isDone(self):
        return libQuickTime.IsMovieDone(self)

    def ptInMovie(self):
        return libQuickTime.PtInMovie(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _availFrame = 0
    def _onImageAvailable(self, visualContext, syncTimeStamp, userParam):
        self._availFrame += 1

    def _setupImageAvailableCB(self):
        QTVisualContextImageAvailableCallback = ctypes.CFUNCTYPE(None, c_void_p, c_uint32, c_void_p)
        onImageAvailableCallback = QTVisualContextImageAvailableCallback(self._onImageAvailable)
        libQuickTime.QTVisualContextSetImageAvailableCallback(self.visualContext, onImageAvailableCallback, None)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

