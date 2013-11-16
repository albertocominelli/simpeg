import unittest
from SimPEG import Solver
from SimPEG.mesh import TensorMesh
from SimPEG.utils import sdiag
import numpy as np
import scipy.sparse as sp
from SimPEG import inverse
from SimPEG.tests import getQuadratic, Rosenbrock

TOL = 1e-2

class TestOptimizers(unittest.TestCase):

    def setUp(self):
        self.A = sp.identity(2).tocsr()
        self.b = np.array([-5,-5])

    def test_GN_Rosenbrock(self):
        GN = inverse.GaussNewton()
        xopt = GN.minimize(Rosenbrock,np.array([0,0]))
        x_true = np.array([1.,1.])
        print 'xopt: ', xopt
        print 'x_true: ', x_true
        self.assertTrue(np.linalg.norm(xopt-x_true,2) < TOL, True)

    def test_GN_quadratic(self):
        GN = inverse.GaussNewton()
        xopt = GN.minimize(getQuadratic(self.A,self.b),np.array([0,0]))
        x_true = np.array([5.,5.])
        print 'xopt: ', xopt
        print 'x_true: ', x_true
        self.assertTrue(np.linalg.norm(xopt-x_true,2) < TOL, True)

    def test_ProjGradient_quadraticBounded(self):
        PG = inverse.ProjectedGradient()
        PG.lower, PG.upper = -2, 2
        xopt = PG.minimize(getQuadratic(self.A,self.b),np.array([0,0]))
        x_true = np.array([2.,2.])
        print 'xopt: ', xopt
        print 'x_true: ', x_true
        self.assertTrue(np.linalg.norm(xopt-x_true,2) < TOL, True)

    def test_ProjGradient_quadratic1Bound(self):
        myB = np.array([-5,1])
        PG = inverse.ProjectedGradient()
        PG.lower, PG.upper = -2, 2
        xopt = PG.minimize(getQuadratic(self.A,myB),np.array([0,0]))
        x_true = np.array([2.,-1.])
        print 'xopt: ', xopt
        print 'x_true: ', x_true
        self.assertTrue(np.linalg.norm(xopt-x_true,2) < TOL, True)

if __name__ == '__main__':
    unittest.main()
