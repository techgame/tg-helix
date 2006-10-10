#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import unittest

from TG.helixui.geometry import geometry

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class TestGeometry(unittest.TestCase):
    def testVecZeros(self):
        v = geometry.vecZeros(size=3)
        self.assertEqual(v.tolist(), [[0., 0., 0.]])
    def testVecOnes(self):
        v = geometry.vecOnes(size=3)
        self.assertEqual(v.tolist(), [[1., 1., 1.]])
    def testVec(self):
        v = geometry.vec([2., 3., 4.])
        self.assertEqual(v.tolist(), [[2., 3., 4.]])
    def testAxisBoxCorners(self):
        v0 = geometry.vec([-1, -1, -1])
        v1 = geometry.vec([2, 3, 4])
        abox = geometry.axisBoxFromCorners(v0, v1)
        self.assertEqual(abox.v.tolist(), v0.tolist()+v1.tolist())
        self.assertEqual(abox.vRect().tolist(), [
                [-1.0, -1.0, -1.0],
                [2.0, -1.0, -1.0],
                [2.0, 3.0, 4.0],
                [-1.0, 3.0, 4.0], ])
        self.assertEqual(abox.vBox().tolist(), [
                [-1.0, -1.0, -1.0],
                [2.0, -1.0, -1.0],
                [2.0, 3.0, -1.0],
                [-1.0, 3.0, -1.0],

                [-1.0, -1.0, 4.0],
                [2.0, -1.0, 4.0],
                [2.0, 3.0, 4.0],
                [-1.0, 3.0, 4.0], ])

    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Unittest Main 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__=='__main__':
    unittest.main()

