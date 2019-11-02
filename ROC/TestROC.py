# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 15:39:18 2013

@author: abraha84
"""

# Unit tests for ROC.py

from __future__ import division
import ROC
import unittest

class TestROC(unittest.TestCase):
    def setUp(self):
        self.nDigitsPrecision = 8
    
    def tearDown(self):
        pass
    
    def testPredictionsAreAllDistinct(self):
        """Test AUC and slope computations when all input predictions are distinct
        """
        r = ROC.ROC([-1,-1,+1,+1],[-1.0, 0.5, -0.5, 1.0], True)
        self.assertAlmostEqual( r.AUC, 0.75  , self.nDigitsPrecision )
      
        self.assertTrue( r.__str__() )
        r.plot( True, False,"Plot title" )
        
    def testPredictionsAreAllSame(self):
        """Test AUC and slope computations when all predicted values coincide
        """
        r = ROC.ROC([-1,-1,+1,+1],[0.5, 0.5, 0.5, 0.5], True)
        self.assertAlmostEqual( r.AUC,  0.0, self.nDigitsPrecision )
        self.assertTrue( r.__str__() )
        r.plot( True, False,"Plot title" )
        
    def testPredictionsNotUnique(self):
        """Test AUC and slope computations when some predicted values coincide
        """
        r = ROC.ROC([-1,-1,+1,-1],[0.0, 0.11, 0.11, 0.12], True)
        self.assertAlmostEqual( r.AUC,  1/3, self.nDigitsPrecision )
        self.assertTrue( r.__str__() )
        r.plot( True, False,"Plot title" )

    
if __name__ == '__main__':
    unittest.main()


