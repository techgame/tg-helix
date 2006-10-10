#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy
from numpy import array, vstack, zeros, ones

from geometryBase import GeometryBase
from boxes import AxisBox

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class GeometryFactory(object):
    dtype = numpy.dtype(numpy.float32)

    _instance = None
    @classmethod
    def singleton(klass):
        result = klass._instance
        if result is None:
            result = object.__new__(klass)
            klass._instance = result
        return result

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def vecZeros(self, count=1, size=3):
        return zeros((count, size), dtype=self.dtype)
    def vecOnes(self, count=1, size=3):
        return ones((count, size), dtype=self.dtype)
    def vec(self, v, size=3):
        return array([v], dtype=self.dtype, ndmin=size-1)

    def axisBoxFromDims(self, w, h, d=2):
        return AxisBox.fromDims(w, h, d)
    def axisBoxFromSize(self, w, h, d=1):
        return AxisBox.fromSize(w, h, d)
    def axisBoxFromCorners(self, v0, v1):
        return AxisBox.fromCorners(v0, v1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GeometryBase.geom = GeometryFactory.singleton()
geometry = GeometryBase.geom

