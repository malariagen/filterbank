import unittest
from os import path
from filterbank.tabfile import Reader

class TestReader(unittest.TestCase):
    def testReader(self):
        reader = Reader(path.join(path.dirname(__file__), 'fixtures', 'test.tab'))
        self.assertEqual(['position','random','sine'], reader.field_names)
        self.assertEqual({'position': 1.0, 'random': 69.0, 'sine': 0.8414709848}, next(reader))
        self.assertEqual({'position': 2.0, 'random': 82.0, 'sine': 0.9092974268}, next(reader))