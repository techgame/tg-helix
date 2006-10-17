#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy
from numpy import array, vstack, zeros, ones

from geometryBase import GeometryBase

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class AxisBox(GeometryBase):
    v = None # array of 2 opposing axis corners, and 1 of the difference in the corners

    def copy(self):
        result = self.__class__()
        result.v = self.v.copy()

    @classmethod
    def fromPos(klass, v, size):
        v0 = klass.geom.vec(v)
        size = klass.geom.vec(size)
        return klass.fromCorners(v0, v0+size)

    @classmethod
    def fromSize(klass, w, h, d=1):
        v0 = klass.geom.vecZeros(size=3)
        v1 = klass.geom.vec([w, h, d])
        return klass.fromCorners(v0, v1)

    @classmethod
    def fromDims(klass, w, h, d=2):
        v = klass.geom.vec([w/2., h/2., d/2.])
        return klass.fromCorners(-v, v)

    @classmethod
    def fromCorners(klass, v0, v1):
        v = vstack([v0, v1])
        v = vstack([v, [v[1]-v[0]]])
        self = klass()
        self.v = v
        return self

    @property
    def size(self):
        return self.v[-1]

    @property
    def whAspect(self):
        size = self.size
        return size[0]/size[1]
    @property
    def wdAspect(self):
        size = self.size
        return size[0]/size[2]
    @property
    def hdAspect(self):
        size = self.size
        return size[1]/size[2]
    @property
    def width(self): return self.size[0]
    @property
    def height(self): return self.size[1]
    @property
    def depth(self): return self.size[2]

    def vRect(self, fillZ=True):
        # duplicate v to make a rectangle
        r = self.v[:-1].repeat(2, 0)
        r[1,0] = r[2,0]
        r[3,0] = r[0,0]
        if fillZ:
            r[:,2] = r[0,2]
        return r
        
    def vBox(self):
        rBottom = self.vRect(False)
        # copy the bottom to make a top
        rTop = rBottom.copy()
        # now fill the z-coord across the bottom 
        rBottom[:,2] = rBottom[0,2]
        # and fill across the top
        rTop[:,2] = rTop[2,2]
        return vstack([rBottom, rTop])

