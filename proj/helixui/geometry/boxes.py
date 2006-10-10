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
    @classmethod
    def fromSize(klass, w, h, d=1):
        v0 = klass.geom.vecZeros(size=3)
        v1 = klass.geom.vec([w, h, d])
        return klass.fromCorners(v0, v1)

    @classmethod
    def fromCorners(klass, v0, v1):
        self = klass()
        v = vstack([v0, v1])
        self.v = v
        self.size = v[1] - v[0]
        return self

    @property
    def width(self): return self.size[0]
    @property
    def height(self): return self.size[1]
    @property
    def depth(self): return self.size[2]

    def vRect(self, fillZ=False):
        # duplicate v0 four times to make a rectangle
        r = self.v.repeat(2, 0)
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

