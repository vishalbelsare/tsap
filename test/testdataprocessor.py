import unittest
import math
import numpy as np
import sys
if "../" not in sys.path:
  sys.path.append("../")
import tsap.data_processor as dp



class TestDataProcessor(unittest.TestCase):
    def testGetReturn1(self):
        """test get_return with a row vector whose elements are all 1.0"""
        x = np.array([np.repeat(1.0,10)])
        y = dp.get_return(x)
        z = np.array([np.repeat(0.0,9)])
        np.testing.assert_array_almost_equal(y,z)

    def testGetReturn2(self):
        """test get_return with a row vector whose elements are not the same"""
        x = np.array([[1.0, 2.0, 3.0, 9.0, 18.0]])
        y = dp.get_return(x)
        z = np.array([[1.0, 0.5, 2.0, 1.0]])
        np.testing.assert_array_almost_equal(y,z)

    def testGetReturn3(self):
        """test get_return with a matrix"""
        x = np.array([[1.0, 2.0], [3.0, 9.0]])
        y = dp.get_return(x)
        z = np.array([[1.0], [2.0]])
        np.testing.assert_array_almost_equal(y,z)

    def testGetReturn4(self):
        """test get_return with a larger matrix"""
        x = np.array([[1.0, 2.0, 3.0, 9.0], [3.0, 9.0, 9.0, 10.8], [1.2, 6.0, 7.2, 14.4]])
        y = dp.get_return(x)
        z = np.array([[1.0, 0.5, 2.0], [2.0, 0.0, 0.2], [4.0, 0.2, 1.0]])
        np.testing.assert_array_almost_equal(y,z)

    ###################################################################


    def testGetPrice1(self):
        """test get_price with a row vector whose elements are all 1.0"""
        x = np.array([np.repeat(0.0,9)])
        s = 1.0
        y = dp.get_price(s,x)
        z = np.array([np.repeat(1.0,9)])
        np.testing.assert_array_almost_equal(y,z)

    def testGetPrice2(self):
        """test get_price with a row vector whose elements are not the same"""
        x = np.array([[1.0, 0.5, 2.0, 1.0]])
        s = 1.0
        y = dp.get_price(s,x)
        z = np.array([[2.0, 3.0, 9.0, 18.0]])
        np.testing.assert_array_almost_equal(y,z)
    
    def testGetPrice3(self):
        """test get_price with a row vector whose elements are not the same, can be negative"""
        x = np.array([[1.0, -0.5, -0.5, 3.0]])
        s = 1.0
        y = dp.get_price(s,x)
        z = np.array([[2.0, 1.0, 0.5, 2.0]])
        np.testing.assert_array_almost_equal(y,z)

    ###################################################################

    def testMaxDrawdown1(self):
        """test max_drawdown with upper trend"""
        x = np.array([[1.0, 2.0, 3.0, 8.0]])
        y = dp.max_drawdown(x)
        self.assertEqual(y,-0.875)

    def testMaxDrawdown2(self):
        """test max_drawdown with lower trend"""
        x = np.array([[10.0, 8.0, 7.0, 7.0]])
        y = dp.max_drawdown(x)
        self.assertEqual(y,-0.3)   

    def testMaxDrawdown3(self):
        """test max_drawdown with peak and trough"""
        x = np.array([[10.0, 1.0, 12.0, 7.0, 7.0, 4.0, 16.0, 10.0, 8.0]])
        y = dp.max_drawdown(x)
        self.assertEqual(y,-15.0/16.0)  

   ###################################################################

    def testGetIndicator1(self):
        """test get_indicator with upper trend"""
        x = np.array([[1.0, 3.0, 5.0, 7.0]])
        y = dp.get_indicator(x)
        z = np.array([[1, 0, 0, -1]])
        np.testing.assert_array_almost_equal(y,z)

    def testGetIndicator2(self):
        """test get_indicator with lower trend"""
        x = np.array([[10.0, 8.0, 6.0, 4.0, 2.0]])
        y = dp.get_indicator(x)
        z = np.zeros((1,5))
        np.testing.assert_array_almost_equal(y,z)

    def testGetIndicator3(self):
        """test get_indicator without trend, trough before peak"""
        x = np.array([[2.0, 8.5, 6.0, 3.0, 10.0, 1.5, 23.0, 7.5]])
        y = dp.get_indicator(x)
        z = np.array([[0, 0, 0, 0, 0, 1, -1, 0]])
        np.testing.assert_array_almost_equal(y,z)

    def testGetIndicator4(self):
        """test get_indicator without trend, trough after peak"""
        x = np.array([[2.0, 8.5, 6.0, 3.0, 10.0, 1.5, 2.3, 7.5]])
        y = dp.get_indicator(x)
        z = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])
        np.testing.assert_array_almost_equal(y,z)


if __name__ == "__main__":
    unittest.main()
