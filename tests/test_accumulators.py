import unittest

import filterbank.accumulators as accumulators

class TestAccumulators(unittest.TestCase):
    def test_dynamic_load(self):
        self.assertEqual(type(accumulators('LastVal')), accumulators.LastVal)
        a = accumulators({'Median':{'test':'foobar'}})
        self.assertEqual(type(a), accumulators.Median)
        self.assertEqual(a.test, 'foobar')

    def testLastVal(self):
        a = accumulators('LastVal')
        self.assertIsNone(a.result())
        a(5)
        self.assertEqual(5,a.result())
        a(4)
        a(3)
        self.assertEqual(3,a.result())
        a.reset()
        self.assertIsNone(a.result())

    def testGeometricMean(self):
        a = accumulators('GeometricMean')
        self.assertIsNone(a.result())
        a(4)
        self.assertEqual(4,a.result())
        a(2)
        self.assertRaises(ValueError, lambda: a(-3))
        self.assertEqual(2.8284271247461903,a.result())
        a.reset()
        self.assertIsNone(a.result())

    def testArithmeticMean(self):
        a = accumulators('ArithmeticMean')
        self.assertIsNone(a.result())
        a(4)
        self.assertEqual(4,a.result())
        a(2)
        a(-3)
        self.assertEqual(1,a.result())
        a.reset()
        self.assertIsNone(a.result())

    def testMedian(self):
        a = accumulators('Median')
        self.assertIsNone(a.result())
        a(4)
        self.assertEqual(4,a.result())
        a(2)
        a(-3)
        self.assertEqual(2,a.result())
        a(-5)
        self.assertEqual(-0.5,a.result())
        a.reset()
        self.assertIsNone(a.result())

    def testPercentile(self):
        a = accumulators({'Percentile':{'percent':0.25}})
        self.assertIsNone(a.result())
        a(4)
        self.assertEqual(4,a.result())
        a(2)
        a(0)
        self.assertEqual(1,a.result())
        a(-5)
        a(-1)
        self.assertEqual(-1,a.result())
        a.reset()
        self.assertIsNone(a.result())

    def testMin(self):
        a = accumulators('Min')
        self.assertEqual(float('inf'),a.result())

        a(5)
        self.assertEqual(5,a.result())
        a(4)
        a(3)
        self.assertEqual(3,a.result())
        a.reset()
        self.assertEqual(float('inf'),a.result())


    def testMax(self):
        a = accumulators('Max')
        self.assertEqual(float('-inf'),a.result())
        a(5)
        self.assertEqual(5,a.result())
        a(4)
        a(3)
        a(6)
        self.assertEqual(6,a.result())
        a.reset()
        self.assertEqual(float('-inf'),a.result())

