import unittest
import contextlib
import os
from os import path
from filterbank.tab_processor import Reader, Writer

class TestReader(unittest.TestCase):
    def testReader(self):
        reader = Reader(path.join(path.dirname(__file__), 'fixtures', 'test.tab'))
        self.assertEqual(['Position','Random','Sine'], reader.field_names)
        self.assertEqual(['1', '69', '0.8414709848'], next(reader))